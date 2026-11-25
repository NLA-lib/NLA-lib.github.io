"""Authenticated editorial workflow and community records, independent of published content."""
import copy
from datetime import datetime, timezone
import re
import secrets
import time
import uuid
from urllib.parse import parse_qs
from urllib.error import HTTPError

from content import UUID, REACTIONS, Snapshot, digest, markdown, packed, preview
from documents import Conflict, Documents
from publisher import PublishingError
from store import fingerprint


class ApiError(Exception):
    def __init__(self,status,message):self.status,self.message=status,message


def public(person):
    return {key:person.get(key,'') for key in ('id','kind','display_name','orcid','bio','affiliation','interests','website')} | {
        'url':'/explore/community/?profile='+person['id'], 'owner_id':person.get('owner_id'),'orcid_verified':person['kind']=='person'}


class Collaboration:
    def __init__(self,auth,documents,snapshot=None,publisher=None,clock=time.time):
        self.auth,self.db=auth,documents
        self.snapshot=snapshot or Snapshot();self.publisher=publisher;self.clock=clock

    def now(self):return datetime.fromtimestamp(self.clock(),timezone.utc).isoformat()

    def attribution(self,actor,person):return {'actor':public(actor),'responsible_person':public(person)}

    def require(self,person,role=None):
        if not person or person.get('status')!='active':raise ApiError(401,'Sign in with ORCID to contribute.')
        if role and person.get('role') not in role:raise ApiError(403,'An editor role is required for this action.')

    def state(self,oid,person=None,revision=None):
        try:state=self.snapshot.get(oid)
        except HTTPError as error:
            if error.code!=404:raise
            state=None
        if revision and state and revision==state['revision']:
            state.update(html=markdown(state['object']['body_markdown']),draft=None)
            return state
        if revision:
            row=self.db.get('ENTRY#'+oid,'REV#'+revision)
            if not row:raise ApiError(404,'Revision not found.')
            if row['status']!='published' and (not person or person['id']!=row['responsible_person_id']) and (not person or person.get('role') not in {'trusted_editor','admin'}):
                raise ApiError(403,'This proposed revision is private to its contributor and editors.')
            return {'object':row['object'],'revision':row['id'],'baseline':row['base_revision'],
                'document_markdown':row['document_markdown'],'source_markdown':row.get('base_document',''),
                'editable':True,'url':row['url'],'draft':None,'used_by':[], 'dependencies':{},
                'html':markdown(row['object']['body_markdown']),
                'diff': ''.join(__import__('difflib').unified_diff(row.get('base_document','').splitlines(True),row['document_markdown'].splitlines(True),fromfile='Published',tofile='Proposed'))}
        if state is None:raise ApiError(404,'Entry not found.')
        state['draft']=None
        if person:
            draft=self.db.get('PERSON#'+person['id'],'DRAFT#'+oid)
            if draft:state['draft']=draft
        state.setdefault('reference_links',{'inherited':[],'editorial':state['object'].get('references',[])})
        return state

    def fresh(self,oid):
        if not re.fullmatch(UUID,oid):raise ValueError('A new statement needs a UUID')
        return {'object':{'id':oid,'type':'statement','title':'New result','body_markdown':'',
            'statement_kind':'result','proofs':[],'references':[],'evidence':{'type':'authored'}},
            'editable':True,'revision':None,'source_sha':None,'source_markdown':'',
            'source_path':'explore/content/statements/result-'+oid+'.md','url':'/explore/statements/'+oid+'/'}

    def meta(self,oid):
        return self.db.get('ENTRY#'+oid,'META') or {'count':0,'reactions':{}}

    def reactions(self,oid,actor=None,meta=None):
        meta=meta or self.meta(oid)
        selected=self.db.get('ENTRY#'+oid,'REACTIONS#'+actor['id']) if actor else None
        return [{'emoji':emoji,'label':label,'count':meta['reactions'].get(emoji,0),
            'reacted':emoji in (selected or {}).get('emojis',[])} for emoji,label in REACTIONS if meta['reactions'].get(emoji,0)]

    def quota(self,person):
        now=int(self.clock())
        self.auth.limit('CONTRIBUTION#'+person['id']+'#'+str(now//3600),120,now+7200)
        self.auth.limit('CONTRIBUTION-DAY#'+str(now//86400),5000,now+172800)

    def activity_change(self,person,actor,oid,state,kind,event_id):
        item={'id':event_id,'actor':public(actor),'responsible_person_id':person['id'],
            'title':state['object']['title'],'url':state['url'],'object_id':oid,'kind':kind,'created_at':self.now()}
        key='ACTIVITY#'+item['created_at']+'#'+event_id
        changes=[('PERSON#'+person['id'],key,item,None),('ENTRY#'+oid,key,item,None)]
        if actor['id']!=person['id']:changes.append(('ACTOR#'+actor['id'],key,item,None))
        return changes

    def auto_follow(self,person,oid,state):
        key='PERSON#'+person['id']
        if self.db.get(key,'FOLLOW#'+oid):return []
        existing,_=self.db.query(key,'FOLLOW#',limit=51)
        if len(existing)>=50:return []
        return [(key,'FOLLOW#'+oid,{'object_id':oid,'title':state['object']['title'],'url':state['url']},None)]

    def propose(self,payload,person,actor):
        if set(payload)!={'idempotency_key','explanation','changes'} or not isinstance(payload['idempotency_key'],str) or not re.fullmatch(r'[A-Za-z0-9-]{8,100}',payload['idempotency_key']):
            raise ValueError('Supply an idempotency key, explanation and changes')
        explanation=payload['explanation']
        if not isinstance(explanation,str) or not 3<=len(explanation.strip())<=2000:raise ValueError('Explain the change in 3–2000 characters')
        changes=payload['changes']
        if not isinstance(changes,list) or not 1<=len(changes)<=5:raise ValueError('A contribution can change 1–5 entries')
        pid=str(uuid.uuid5(uuid.NAMESPACE_URL,person['id']+':'+actor['id']+':'+payload['idempotency_key']))
        previous=self.db.get('PROPOSAL#'+pid,'META')
        request_hash=digest(payload)
        if previous:
            if previous['request_hash']!=request_hash:raise Conflict('This idempotency key was used for different content')
            return previous
        proposal={'id':pid,'request_hash':request_hash,'explanation':explanation.strip(),'status':'submitted',
            'attribution':self.attribution(actor,person),'responsible_person_id':person['id'],
            'created_at':self.now(),'revisions':{},'objects':[]}
        writes=[];seen=set()
        parent_snapshot=self.snapshot
        created=[{'id':x.get('id'),'statement_id':'result-'+x['id']} for x in changes
                 if isinstance(x,dict) and x.get('operation')=='create_statement' and isinstance(x.get('id'),str)]
        class StagedSnapshot:
            def index(self):return parent_snapshot.index()+created
            def references(self):return parent_snapshot.references()
        validation_snapshot=StagedSnapshot()
        for change in changes:
            if not isinstance(change,dict) or set(change)!={'operation','id','base_revision','fields'}:raise ValueError('Invalid change fields')
            oid=change['id']
            if oid in seen:raise ValueError('Combine changes to the same entry')
            seen.add(oid)
            if change['operation']=='create_statement':
                state=self.fresh(oid)
                try:self.snapshot.get(oid)
                except HTTPError as error:
                    if error.code!=404:raise
                else:raise Conflict('This statement already exists')
            else:state=self.state(oid,person)
            if change['operation'] not in {'create_statement','update_'+state['object']['type']}:raise ValueError('Invalid operation')
            if state['revision']!=change['base_revision']:raise Conflict('Published content changed. Compare your draft with the latest source before submitting.')
            checked=preview(validation_snapshot,state,change['fields'])
            if checked['document_markdown']==state.get('source_markdown'):raise ValueError('There are no changes to submit')
            rid=str(uuid.uuid4());proposal['revisions'][oid]=rid
            proposal['objects'].append({'id':oid,'title':checked['object']['title'],'revision':rid})
            revision={'id':rid,'object_id':oid,'proposal_id':pid,'status':'submitted','object':checked['object'],
                'base_revision':state['revision'],'base_source_sha':state.get('source_sha'),
                'base_document':state.get('source_markdown',''),'source_path':state['source_path'],
                'document_markdown':checked['document_markdown'],'created_at':self.now(),
                'explanation':explanation,'attribution':proposal['attribution'],'responsible_person_id':person['id'],'url':state['url']}
            revision['history_key']='HISTORY#'+revision['created_at']+'#'+rid
            history={k:v for k,v in revision.items() if k in {'id','created_at','explanation','attribution','status','responsible_person_id','proposal_id'}}
            writes.append(('ENTRY#'+oid,revision['history_key'],history,None))
            if len(packed(revision).encode())>380_000:raise ValueError('This revision is too large; split it into smaller edits')
            if state['revision'] and not self.db.get('ENTRY#'+oid,'REV#'+state['revision']):
                baseline={'id':state['revision'],'object_id':oid,'status':'published','object':state['object'],
                    'document_markdown':state.get('document_markdown',state.get('source_markdown','')),
                    'base_revision':state['revision'],'url':state['url'],'base_document':'',
                    'responsible_person_id':person['id'],'explanation':'Published source baseline','created_at':self.now()}
                writes.append(('ENTRY#'+oid,'REV#'+state['revision'],baseline,None))
                writes.append(('ENTRY#'+oid,'HISTORY#'+self.now()+'#'+state['revision'],{k:v for k,v in baseline.items() if k in {'id','status','created_at','explanation','responsible_person_id'}},None))
            writes.append(('ENTRY#'+oid,'REV#'+rid,revision,None))
            writes.extend(x for x in self.activity_change(person,actor,oid,state,'proposal',rid) if not x[0].startswith('ENTRY#'))
            if actor['kind']=='person':writes.extend(self.auto_follow(person,oid,state))
        writes.extend([('PROPOSAL#'+pid,'META',proposal,None),
            ('PERSON#'+person['id'],'PROPOSAL#'+proposal['created_at']+'#'+pid,{'id':pid},None),
            ('REVIEW','PROPOSAL#'+proposal['created_at']+'#'+pid,{'id':pid},None)])
        self.db.commit(writes)
        return proposal

    def proposal(self,pid,person):
        if not re.fullmatch(UUID,pid):raise ValueError('Invalid proposal ID')
        result=self.db.get('PROPOSAL#'+pid,'META')
        if not result:raise ApiError(404,'Contribution not found')
        if result['responsible_person_id']!=person['id'] and person.get('role') not in {'trusted_editor','admin'}:
            raise ApiError(403,'This contribution is private to its contributor and editors')
        return result

    def review(self,pid,payload,person):
        self.require(person,{'trusted_editor','admin'})
        proposal=self.proposal(pid,person)
        if set(payload)!={'decision','message'} or payload['decision'] not in {'approve','reject','request_changes'} or not isinstance(payload['message'],str) or len(payload['message'])>2000:
            raise ValueError('Choose approve, reject or request_changes and supply a short message')
        if proposal['status'] not in {'submitted','changes_requested'}:raise Conflict('This contribution has already been reviewed')
        proposal.update(status={'approve':'approved','reject':'rejected','request_changes':'changes_requested'}[payload['decision']],
            reviewer=public(person),review_message=payload['message'],reviewed_at=self.now())
        self.db.commit([('PROPOSAL#'+pid,'META',proposal,proposal['_version'])])
        return proposal

    def publish(self,pid,person):
        self.require(person,{'trusted_editor','admin'})
        if not self.publisher:raise ApiError(503,'The GitHub App has not been connected yet. Your approved contribution is saved.')
        proposal=self.proposal(pid,person)
        if proposal['status']=='published':return proposal
        if proposal['status'] not in {'approved','awaiting_checks'}:raise Conflict('Approve this contribution before publishing')
        revisions=[self.db.get('ENTRY#'+oid,'REV#'+rid) for oid,rid in proposal['revisions'].items()]
        if not proposal.get('pull_request'):
            proposal['pull_request']=self.publisher.open(proposal,revisions)
            proposal['status']='awaiting_checks'
            self.db.commit([('PROPOSAL#'+pid,'META',proposal,proposal['_version'])])
            proposal=self.proposal(pid,person)
        result=self.publisher.merge(proposal['pull_request'])
        if result['merged']:
            proposal.update(status='published',commit=result['sha'],published_at=self.now())
            writes=[('PROPOSAL#'+pid,'META',proposal,proposal['_version'])]
            for revision in revisions:
                revision.update(status='published',commit=result['sha'])
                writes.append(('ENTRY#'+revision['object_id'],'REV#'+revision['id'],revision,revision['_version']))
                history=self.db.get('ENTRY#'+revision['object_id'],revision['history_key'])
                history.update(status='published',commit=result['sha'])
                writes.append(('ENTRY#'+revision['object_id'],revision['history_key'],history,history['_version']))
                writes.extend(self.activity_change(proposal['attribution']['responsible_person'],proposal['attribution']['actor'],revision['object_id'],{'object':revision['object'],'url':revision['url']},'revision','published-'+revision['id']))
            self.db.commit(writes)
        return proposal

    def handle(self,method,path,query,payload,session,authorization=''):
        person=session['person'] if session else None
        actor=person;bot=False
        if authorization:
            if not authorization.startswith('Bearer '):raise ApiError(401,'Invalid bot credential')
            auth=self.db.get('TOKEN#'+fingerprint(authorization[7:]),'AUTH')
            if not auth or auth.get('revoked') or auth['expires_at']<=self.clock():raise ApiError(401,'Invalid, expired or revoked bot token')
            person=self.auth.person(auth['responsible_person_id']);self.require(person)
            actor=auth['actor'];bot=True
            private=path.startswith(('me/','notifications','bots','proposals/','review')) or path=='bootstrap' or (path=='proposals' and method=='GET') or path.endswith(('/draft','/follow'))
            if private:raise ApiError(403,'Bot credentials cannot access private person data or review tools')
            if method=='POST':
                scope='feedback' if path=='feedback/preview' or path.endswith('/feedback') else 'proposals' if path=='proposals' or path.endswith('/preview') or path=='preview' else 'reactions' if path.endswith('/reaction') else ''
                if scope not in auth['scopes']:raise ApiError(403,'This token does not permit that action')
        if path=='bootstrap' and method=='GET':
            return {'session':session['record']['csrf'] if session else '', 'person':public(person) if person else None,
                'role':person.get('role','contributor') if person else None,'reaction_options':[{'emoji':e,'label':l} for e,l in REACTIONS],
                'hosted':True,'features':['editing','review','discussions','reactions','drafts','bots'], 'publishing':bool(self.publisher)}
        if method=='POST':
            self.require(person)
            if path.endswith('preview'):
                now=int(self.clock());self.auth.limit('PREVIEW#'+person['id']+'#'+str(now//3600),600,now+7200)
            else:self.quota(person)
        query=parse_qs(query)
        cursor=query.get('cursor',[None])[0]
        if cursor=='0':cursor=None
        if cursor and (len(cursor)>300 or '\x00' in cursor):raise ValueError('Invalid cursor')
        if path=='schema':
            return {'schema_version':1,'operations':['update_page','update_statement','create_statement'],
                'change':{'operation':'update_page','id':'UUID','base_revision':'published revision token','fields':{'document_markdown':'complete source'}},
                'submission':{'idempotency_key':'unique request ID','explanation':'reason for change','changes':'1–5 changes'},
                'workflow':'draft → submitted → approved → awaiting_checks → published','authentication':'ORCID cookie + X-CSRF-Token, or scoped bot Bearer token'}
        if path=='references':
            refs=self.snapshot.references();return {'references':[dict(value,key=key) for key,value in refs.items()]}
        if path=='objects' and method=='GET':
            q=query.get('q',[''])[0].lower();kind=query.get('type',[''])[0]
            objects=[x for x in self.snapshot.index() if (not kind or x['type']==kind) and (kind!='statement' or x.get('statement_id')) and q in x['title'].lower()]
            start=int(cursor or 0);limit=min(100,max(1,int(query.get('limit',['100'])[0])))
            return {'objects':objects[start:start+limit],'next_cursor':str(start+limit) if start+limit<len(objects) else None}
        if path=='activity' and method=='GET':
            ids=query.get('ids',[''])[0].split(',')
            if len(ids)>200 or any(not re.fullmatch(UUID,oid) for oid in ids):raise ValueError('Supply up to 200 entry IDs')
            keys=[('ENTRY#'+oid,'META') for oid in ids]
            if actor:keys.extend(('ENTRY#'+oid,'REACTIONS#'+actor['id']) for oid in ids)
            rows=self.db.many(list(dict.fromkeys(keys)))
            result={}
            for oid in ids:
                meta=rows.get(('ENTRY#'+oid,'META'),{'count':0,'reactions':{}})
                selected=rows.get(('ENTRY#'+oid,'REACTIONS#'+actor['id']),{}) if actor else {}
                reactions=[{'emoji':emoji,'label':label,'count':meta['reactions'].get(emoji,0),'reacted':emoji in selected.get('emojis',[])}
                    for emoji,label in REACTIONS if meta['reactions'].get(emoji,0)]
                result[oid]={'count':meta['count'],'reactions':reactions}
            return {'objects':result}
        if path=='feedback/preview' and method=='POST':
            if set(payload)!={'body'} or not isinstance(payload['body'],str) or len(payload['body'])>10000:raise ValueError('Invalid message')
            return {'html':markdown(payload['body'])}
        if path=='preview' and method=='POST':return preview(self.snapshot,self.fresh(str(uuid.uuid4())),payload.get('fields'))
        if path=='proposals':
            self.require(person)
            if method=='POST':return self.propose(payload,person,actor)
            refs,next_cursor=self.db.query('PERSON#'+person['id'],'PROPOSAL#',cursor=cursor,reverse=True)
            return {'items':[self.proposal(x['id'],person) for x in refs],'next_cursor':next_cursor}
        match=re.fullmatch(r'proposals/('+UUID+r')(?:/(review|publish))?',path)
        if match:
            self.require(person)
            if method=='GET' and not match[2]:return self.proposal(match[1],person)
            if method=='POST' and match[2]=='review':return self.review(match[1],payload,person)
            if method=='POST' and match[2]=='publish':return self.publish(match[1],person)
        if path=='review' and method=='GET':
            self.require(person,{'trusted_editor','admin'})
            refs,next_cursor=self.db.query('REVIEW','PROPOSAL#',cursor=cursor,reverse=True)
            return {'items':[self.proposal(x['id'],person) for x in refs],'next_cursor':next_cursor}
        match=re.fullmatch(r'objects/('+UUID+r')(?:/(draft|preview|history|feedback|reaction|follow|report))?',path)
        if match:
            oid,action=match.groups()
            revision=query.get('revision',[None])[0]
            state=self.state(oid,None if bot else person,revision)
            if method=='GET':
                if action is None:return state
                if action=='history':
                    rows,next_cursor=self.db.query('ENTRY#'+oid,'HISTORY#',cursor=cursor,reverse=True)
                    rows=[x for x in rows if x['id']!=state['revision'] and (x['status']=='published' or (person and (x['responsible_person_id']==person['id'] or person.get('role') in {'trusted_editor','admin'})))]
                    return {'revisions':[{'id':state['revision'],'baseline':True,'explanation':'Published source','source_sha':state.get('source_sha')},
                        *[{k:v for k,v in row.items() if k in {'id','created_at','explanation','attribution','status','commit','proposal_id'}} for row in rows]],'next_cursor':next_cursor}
                if action=='feedback':
                    meta=self.meta(oid)
                    if query.get('summary')==['1']:return {'count':meta['count']}
                    rows,next_cursor=self.db.query('ENTRY#'+oid,'COMMENT#',cursor=cursor)
                    return {'items':rows,'count':meta['count'],'next_cursor':next_cursor,'reactions':self.reactions(oid,actor,meta)}
                if action=='reaction':return {'reactions':self.reactions(oid,actor)}
                if action=='follow':return {'following':bool(person and self.db.get('PERSON#'+person['id'],'FOLLOW#'+oid))}
            if method=='POST':
                if action=='preview':return preview(self.snapshot,state,payload.get('fields'))
                if action=='draft':
                    if set(payload)-{'base_revision','fields','draft_revision'} or not {'base_revision','fields'}<=payload.keys():raise ValueError('Invalid draft fields')
                    if payload['base_revision']!=state['revision']:raise Conflict('Published content changed; compare before saving')
                    previous=self.db.get('PERSON#'+person['id'],'DRAFT#'+oid)
                    if payload.get('draft_revision')!=(previous or {}).get('draft_revision'):raise Conflict('Your draft changed in another editor')
                    checked=preview(self.snapshot,state,payload['fields'])
                    result={'object':checked['object'],'document_markdown':checked['document_markdown'],
                        'base_revision':state['revision'],'draft_revision':str(uuid.uuid4()),'title':checked['object']['title'],'url':state['url'],'object_id':oid}
                    self.db.commit([('PERSON#'+person['id'],'DRAFT#'+oid,result,(previous or {}).get('_version'))])
                    return result
                if action=='report':
                    if set(payload)!={'comment_id','reason'} or not isinstance(payload['reason'],str) or not 3<=len(payload['reason'])<=2000:
                        raise ValueError('Supply a reason and optional comment_id')
                    cid=payload['comment_id']
                    if cid and (not isinstance(cid,str) or not self.db.get('ENTRY#'+oid,'COMMENT#'+cid)):
                        raise ValueError('Unknown comment on this entry')
                    rid=self.now()+'#'+str(uuid.uuid4())
                    report={'id':rid,'object_id':oid,'comment_id':cid,'reason':payload['reason'],
                        'reporter_id':person['id'],'created_at':self.now(),'title':state['object']['title'],'url':state['url'],'status':'open'}
                    self.db.commit([('MODERATION','REPORT#'+rid,report,None)])
                    return {'reported':True}
                if action=='feedback':
                    if set(payload)!={'kind','body','parent_id'} or payload['kind'] not in {'comment','suggestion','mathematical-error','reference-request','formalization-request','generalization'} or not isinstance(payload['body'],str) or not 1<=len(payload['body'].strip())<=10000:
                        raise ValueError('Invalid discussion message')
                    parent=payload['parent_id']
                    if parent and (not isinstance(parent,str) or not self.db.get('ENTRY#'+oid,'COMMENT#'+parent)):raise ValueError('Reply must reference a comment on this entry')
                    cid=self.now()+'#'+str(uuid.uuid4())
                    item={'id':cid,'kind':payload['kind'],'body':payload['body'].strip(),'html':markdown(payload['body'].strip()),
                        'parent_id':parent,'created_at':self.now(),'revision':state['revision'],'attribution':self.attribution(actor,person)}
                    meta=self.meta(oid);meta['count']+=1
                    self.db.commit([('ENTRY#'+oid,'COMMENT#'+cid,item,None),('ENTRY#'+oid,'META',meta,meta.get('_version')),
                        *self.activity_change(person,actor,oid,state,'comment',cid),
                        *(self.auto_follow(person,oid,state) if actor['kind']=='person' else [])])
                    return {'id':cid}
                if action=='reaction':
                    if set(payload)!={'emoji','active'} or payload['emoji'] not in dict(REACTIONS) or not isinstance(payload['active'],bool):raise ValueError('Choose a supported emoji and active boolean')
                    previous=self.db.get('ENTRY#'+oid,'REACTIONS#'+actor['id'])
                    emojis=set((previous or {}).get('emojis',[]));emoji=payload['emoji']
                    if (emoji in emojis)!=payload['active']:
                        meta=self.meta(oid);meta['reactions'][emoji]=max(0,meta['reactions'].get(emoji,0)+(1 if payload['active'] else -1))
                        if payload['active']:emojis.add(emoji)
                        else:emojis.discard(emoji)
                        activity_pk=('PERSON#' if actor['kind']=='person' else 'ACTOR#')+actor['id']
                        activity=self.db.get(activity_pk,'REACTION#'+oid)
                        self.db.commit([('ENTRY#'+oid,'REACTIONS#'+actor['id'],{'emojis':sorted(emojis)},(previous or {}).get('_version')),
                            ('ENTRY#'+oid,'META',meta,meta.get('_version')),
                            (activity_pk,'REACTION#'+oid,{'emojis':sorted(emojis),'title':state['object']['title'],'url':state['url'],'actor':public(actor)},(activity or {}).get('_version'))])
                    return {'reactions':self.reactions(oid,actor)}
                if action=='follow':
                    if set(payload)!={'active'} or not isinstance(payload['active'],bool):raise ValueError('Supply an explicit active boolean')
                    pk='PERSON#'+person['id'];sk='FOLLOW#'+oid;previous=self.db.get(pk,sk)
                    if payload['active'] and not previous:
                        following,_=self.db.query(pk,'FOLLOW#',limit=51)
                        if len(following)>=50:raise ValueError('You can follow up to 50 entries in this first release')
                        self.db.commit([(pk,sk,{'object_id':oid,'title':state['object']['title'],'url':state['url']},None)])
                    elif previous and not payload['active']:self.db.commit([(pk,sk,None,previous['_version'])])
                    return {'following':payload['active']}
        if path=='moderation' and method=='GET':
            self.require(person,{'moderator','admin'})
            items,next_cursor=self.db.query('MODERATION','REPORT#',cursor=cursor,reverse=True)
            return {'items':items,'next_cursor':next_cursor}
        if path=='moderation/resolve' and method=='POST':
            self.require(person,{'moderator','admin'})
            if set(payload)!={'id','action'} or payload['action'] not in {'dismiss','hide_comment'}:
                raise ValueError('Choose dismiss or hide_comment')
            report=self.db.get('MODERATION','REPORT#'+payload['id'])
            if not report:raise ApiError(404,'Report not found')
            writes=[]
            if payload['action']=='hide_comment':
                comment=self.db.get('ENTRY#'+report['object_id'],'COMMENT#'+str(report['comment_id']))
                if not comment:raise ValueError('This report does not refer to a comment')
                original=copy.deepcopy(comment)
                comment.update(body='[Comment removed by a moderator.]',html='<p>Comment removed by a moderator.</p>',hidden=True)
                writes.extend([('ENTRY#'+report['object_id'],'COMMENT#'+report['comment_id'],comment,comment['_version']),
                    ('MODERATION','AUDIT#'+str(uuid.uuid4()),{'comment':original,'moderator_id':person['id'],'report_id':report['id'],'created_at':self.now()},None)])
            report.update(status='resolved',resolution=payload['action'],moderator_id=person['id'])
            writes.append(('MODERATION','REPORT#'+report['id'],report,report['_version']))
            self.db.commit(writes);return {'resolved':True}
        if path=='me/profile' and method=='POST':
            from app import profile_fields
            return public(self.auth.update_profile(person['id'],profile_fields(payload)))
        if path=='me/workspace' and method=='GET':
            self.require(person)
            drafts,dc=self.db.query('PERSON#'+person['id'],'DRAFT#');following,_=self.db.query('PERSON#'+person['id'],'FOLLOW#')
            return {'drafts':[{k:v for k,v in x.items() if k in {'object_id','title','url'}} for x in drafts], 'following':following,'next_cursor':dc}
        if path=='notifications' and method=='GET':
            self.require(person)
            following,_=self.db.query('PERSON#'+person['id'],'FOLLOW#',limit=50)
            items=[]
            for followed in following:
                recent,_=self.db.query('ENTRY#'+followed['object_id'],'ACTIVITY#',limit=10,reverse=True)
                items.extend(x for x in recent if x['responsible_person_id']!=person['id'])
            read,_=self.db.query('PERSON#'+person['id'],'READ#',limit=100)
            ids={x['id'] for x in read}
            items=sorted(items,key=lambda x:x['created_at'],reverse=True)[:100]
            for item in items:item['read_at']=True if item['id'] in ids else None
            return {'items':items,'unread':sum(not x['read_at'] for x in items),'next_cursor':None}
        if path=='notifications/read' and method=='POST':
            if set(payload)!={'id'} or not isinstance(payload['id'],str) or len(payload['id'])>150:raise ValueError('Invalid notification ID')
            pk='PERSON#'+person['id'];sk='READ#'+fingerprint(payload['id']);old=self.db.get(pk,sk)
            self.db.commit([(pk,sk,{'id':payload['id']},(old or {}).get('_version'))]);return {'read':True}
        if path=='bots':
            self.require(person)
            if method=='GET':
                bots,_=self.db.query('PERSON#'+person['id'],'BOT#');return {'bots':[dict(bot=public(x['actor']),token_id=x['token_id'],scopes=x['scopes'],revoked=x['revoked'],expires_at=x['expires_at']) for x in bots]}
            if set(payload)!={'display_name','bio','scopes'} or not isinstance(payload['bio'],str) or len(payload['bio'])>2000 or not isinstance(payload['display_name'],str) or not 1<=len(payload['display_name'].strip())<=100 or not isinstance(payload['scopes'],list) or not payload['scopes'] or set(payload['scopes'])-{'proposals','feedback','reactions'}:raise ValueError('Supply a bot name and supported scopes')
            existing,_=self.db.query('PERSON#'+person['id'],'BOT#',limit=11)
            if len(existing)>=10:raise ValueError('At most 10 bot tokens per person')
            bid=str(uuid.uuid4());token=secrets.token_urlsafe(40)
            bot_actor={'id':bid,'kind':'bot','display_name':payload['display_name'].strip(),'bio':payload['bio'],'owner_id':person['id']}
            record={'actor':bot_actor,'responsible_person_id':person['id'],'scopes':sorted(set(payload['scopes'])),
                'expires_at':int(self.clock())+90*86400,'token_id':bid,'token_hash':fingerprint(token),'revoked':False}
            self.db.commit([('TOKEN#'+fingerprint(token),'AUTH',record,None),('PERSON#'+person['id'],'BOT#'+bid,record,None),('ACTOR#'+bid,'PROFILE',dict(bot_actor,owner=public(person)),None)])
            return {'token':token,'bot':public(bot_actor),'expires_at':record['expires_at']}
        match=re.fullmatch(r'bots/('+UUID+r')/revoke',path)
        if match and method=='POST':
            record=self.db.get('PERSON#'+person['id'],'BOT#'+match[1])
            if not record:raise ApiError(404,'Bot token not found')
            auth=self.db.get('TOKEN#'+record['token_hash'],'AUTH');auth['revoked']=True;record['revoked']=True
            self.db.commit([('PERSON#'+person['id'],'BOT#'+match[1],record,record['_version']),('TOKEN#'+record['token_hash'],'AUTH',auth,auth['_version'])]);return {'revoked':True}
        match=re.fullmatch(r'profiles/('+UUID+r')',path)
        if match and method=='GET':
            profile=self.auth.person(match[1]) or self.db.get('ACTOR#'+match[1],'PROFILE')
            if not profile:raise ApiError(404,'Profile not found')
            activities,next_cursor=self.db.query(('PERSON#' if profile['kind']=='person' else 'ACTOR#')+match[1],'ACTIVITY#',cursor=cursor,reverse=True)
            # Proposed manuscript text and submission activity are private until published.
            activities=[x for x in activities if x['kind'] in {'comment','revision'}]
            bots=[]
            if profile['kind']=='person':
                rows,_=self.db.query('PERSON#'+match[1],'BOT#');bots=[public(x['actor']) for x in rows]
            reaction_rows,_=self.db.query('PERSON#'+match[1],'REACTION#') if profile['kind']=='person' else self.db.query('ACTOR#'+match[1],'REACTION#')
            reactions=[dict(row,emoji=emoji) for row in reaction_rows for emoji in row['emojis']]
            return {'profile':public(profile),'activities':activities,'bots':bots,'reactions':reactions,'next_cursor':next_cursor}
        raise ApiError(404,'API route not found')
