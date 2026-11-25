"""GitHub App publisher: allowlisted content paths, checked PRs and squash merges."""
import base64
import json
import re
import time
from urllib.parse import quote

import requests
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


class PublishingError(Exception):
    pass


class Publisher:
    api='https://api.github.com/repos/NLA-lib/NLA-lib.github.io'
    def __init__(self,secrets,secret_arn,clock=time.time):
        self.secrets,self.secret_arn,self.clock=secrets,secret_arn,clock
        self.token=None;self.expires=0

    def installation_token(self):
        if self.token and self.expires>self.clock()+60:return self.token
        secret=json.loads(self.secrets.get_secret_value(SecretId=self.secret_arn)['SecretString'])
        def encode(raw):return base64.urlsafe_b64encode(raw).rstrip(b'=')
        now=int(self.clock())
        unsigned=encode(b'{"alg":"RS256","typ":"JWT"}')+b'.'+encode(json.dumps({'iat':now-60,'exp':now+540,'iss':str(secret['app_id'])}).encode())
        key=serialization.load_pem_private_key(secret['private_key'].encode(),password=None)
        jwt=(unsigned+b'.'+encode(key.sign(unsigned,padding.PKCS1v15(),hashes.SHA256()))).decode()
        response=requests.post('https://api.github.com/app/installations/'+str(int(secret['installation_id']))+'/access_tokens',
            headers={'Authorization':'Bearer '+jwt,'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'},
            json={'repositories':['NLA-lib.github.io'],'permissions':{'contents':'write','pull_requests':'write','checks':'read','statuses':'read'}},timeout=10,allow_redirects=False)
        if response.status_code!=201:raise PublishingError('GitHub App authentication failed. Check its installation and permissions.')
        self.token=response.json()['token'];self.expires=now+3000
        return self.token

    def request(self,method,path,body=None,allowed=(200,201)):
        response=requests.request(method,self.api+path,headers={'Authorization':'Bearer '+self.installation_token(),
            'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'},json=body,timeout=10,allow_redirects=False)
        if response.status_code not in allowed:
            # Do not propagate GitHub response bodies or tokens into public logs.
            raise PublishingError('GitHub rejected the publication request (HTTP '+str(response.status_code)+'). Repository protections remain in force.')
        return response.json() if response.content else {}

    @staticmethod
    def path(value):
        if not isinstance(value,str) or not re.fullmatch(r'explore/content/(?:[a-z0-9-]+/)*[a-z0-9-]+\.md',value) or value.endswith('/README.md'):
            raise PublishingError('Publication is restricted to mathematical content Markdown.')
        return value

    def open(self,proposal,revisions):
        branch='contributions/'+proposal['id']
        existing=self.request('GET','/pulls?state=all&head=NLA-lib:'+quote(branch,safe=''))
        if existing:
            pr=existing[0]
            return {'number':pr['number'],'url':pr['html_url'],'head':pr['head']['sha'],'title':pr['title'],'message':pr['body']}
        base=self.request('GET','/git/ref/heads/main')['object']['sha']
        commit=self.request('GET','/git/commits/'+base)
        files=[]
        for revision in revisions:
            path=self.path(revision['source_path'])
            current=self.request('GET','/contents/'+path+'?ref='+base,allowed=(200,404))
            if current.get('sha')!=revision.get('base_source_sha'):
                raise PublishingError('Published source changed since this proposal. Rebase and resubmit; nothing was overwritten.')
            files.append({'path':path,'mode':'100644','type':'blob','content':revision['document_markdown']})
        tree=self.request('POST','/git/trees',{'base_tree':commit['tree']['sha'],'tree':files})
        actor=proposal['attribution']['actor'];person=proposal['attribution']['responsible_person']
        message=proposal['explanation']+'\n\nContributor-ORCID: https://orcid.org/'+person['orcid']+'\nRevision: '+proposal['id']+'\n'
        if actor['kind']=='bot':message+='Agent: '+actor['display_name']+'\nResponsible-Person: '+person['display_name']+'\n'
        reviewer=proposal['reviewer'];message+='Reviewed-by: '+reviewer['display_name']+' <https://orcid.org/'+reviewer['orcid']+'>\n'
        author={'name':' '.join(actor['display_name'].split()),'email':person['orcid']+'@noreply.nla-lib.org'}
        message+='Co-authored-by: '+author['name']+' <'+author['email']+'>\n'
        new=self.request('POST','/git/commits',{'message':message,'tree':tree['sha'],'parents':[base],'author':author})
        ref=self.request('GET','/git/ref/heads/'+branch,allowed=(200,404))
        if ref.get('object'):
            # Never force an existing branch, even on a retry.
            if ref['object']['sha']!=new['sha']:
                previous=self.request('GET','/git/commits/'+ref['object']['sha'])
                if previous['tree']['sha']!=tree['sha'] or previous['message']!=message:
                    raise PublishingError('Publication branch already exists. Review it before retrying.')
                new=previous
        else:self.request('POST','/git/refs',{'ref':'refs/heads/'+branch,'sha':new['sha']})
        pr=self.request('POST','/pulls',{'title':proposal['explanation'][:180],'head':branch,'base':'main',
            'body':'Accepted Explorer contribution.\n\n'+message+'\n\nOne squash commit will publish this contribution after repository checks pass.'})
        return {'number':pr['number'],'url':pr['html_url'],'head':new['sha'],'title':proposal['explanation'][:180],'message':message}

    def merge(self,pr):
        current=self.request('GET','/pulls/'+str(pr['number']))
        if current.get('merged'):return {'merged':True,'sha':current['merge_commit_sha']}
        if current['head']['sha']!=pr['head']:raise PublishingError('The publication branch changed. Review it again before merging.')
        checks=self.request('GET','/commits/'+pr['head']+'/check-runs?per_page=100')['check_runs']
        statuses=self.request('GET','/commits/'+pr['head']+'/status')
        if not {'test','Published content build'} <= {x['name'] for x in checks} or any(x['status']!='completed' or x['conclusion'] not in {'success','neutral','skipped'} for x in checks) or (statuses['total_count'] and statuses['state']!='success'):
            return {'merged':False,'status':'awaiting_checks'}
        result=self.request('PUT','/pulls/'+str(pr['number'])+'/merge',{'merge_method':'squash','sha':pr['head'],**({'commit_title':pr['title'],'commit_message':pr['message']} if pr.get('message') else {})})
        return {'merged':bool(result.get('merged')),'sha':result.get('sha'),'status':'awaiting_checks'}
