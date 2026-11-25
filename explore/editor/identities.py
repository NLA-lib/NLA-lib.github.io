"""Local identity prototype. Tokens identify bots; ownership is assigned by the server."""
import hashlib
import json
import secrets
import uuid
from datetime import datetime, timezone
from content_pages import markdown

PERSON = 'local-researcher'

def now():
    return datetime.now(timezone.utc).isoformat()

class IdentityStore:
    def init_identities(self):
        self.db.executescript('''
        CREATE TABLE IF NOT EXISTS actors(id TEXT PRIMARY KEY, kind TEXT NOT NULL,
          owner_id TEXT, profile TEXT NOT NULL, created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS attribution(kind TEXT NOT NULL, target TEXT NOT NULL,
          object_id TEXT NOT NULL, actor_id TEXT NOT NULL, responsible_person_id TEXT NOT NULL,
          created_at TEXT NOT NULL, PRIMARY KEY(kind,target));
        CREATE INDEX IF NOT EXISTS attribution_person ON attribution(responsible_person_id,created_at);
        CREATE TABLE IF NOT EXISTS bot_tokens(id TEXT PRIMARY KEY, bot_id TEXT NOT NULL,
          token_hash TEXT UNIQUE NOT NULL, scopes TEXT NOT NULL, revoked_at TEXT);
        CREATE TABLE IF NOT EXISTS subscriptions(person_id TEXT NOT NULL, object_id TEXT NOT NULL,
          PRIMARY KEY(person_id,object_id));
        CREATE TABLE IF NOT EXISTS notifications(id TEXT PRIMARY KEY, person_id TEXT NOT NULL,
          actor_id TEXT NOT NULL, object_id TEXT NOT NULL, kind TEXT NOT NULL,
          target TEXT NOT NULL, created_at TEXT NOT NULL, read_at TEXT);
        ''')
        self.db.execute('INSERT OR IGNORE INTO actors VALUES(?,?,?,?,?)', (PERSON, 'person', None,
            json.dumps({'display_name': 'Local researcher', 'bio': '', 'affiliation': '', 'interests': '', 'website': '', 'orcid': ''}), now()))
        # Existing local records were all made by the original prototype person.
        for kind, table, column in [('revision','revisions','id'), ('comment','feedback','id')]:
            self.db.execute(f'''INSERT OR IGNORE INTO attribution
                SELECT ?,{column},object_id,?,?,created_at FROM {table}''', (kind,PERSON,PERSON))
        self.db.commit()

    def actor(self, actor_id=PERSON):
        row = self.db.execute('SELECT * FROM actors WHERE id=?', (actor_id,)).fetchone()
        if row is None:
            raise KeyError('Unknown profile')
        return {'id': row['id'], 'kind': row['kind'], 'owner_id': row['owner_id'],
                **json.loads(row['profile']), 'url': '/explore/people/' + row['id'] + '/', 'orcid_verified': False}

    def update_profile(self, fields):
        allowed = {'display_name': 100, 'bio': 2000, 'affiliation': 200, 'interests': 500, 'website': 500, 'orcid': 19}
        if not fields or fields.keys() - allowed.keys():
            raise ValueError('Unknown profile fields')
        profile = {key: value for key, value in self.actor().items() if key in allowed}
        for key, value in fields.items():
            if not isinstance(value, str) or len(value) > allowed[key]:
                raise ValueError('Invalid profile field: ' + key)
            profile[key] = value.strip()
        if not profile['display_name']:
            raise ValueError('A display name is required')
        if profile['website']:
            from urllib.parse import urlsplit
            url = urlsplit(profile['website'])
            if url.scheme != 'https' or not url.hostname or url.username or url.password:
                raise ValueError('Website must be an HTTPS URL')
        if profile['orcid']:
            import re
            if not re.fullmatch(r'\d{4}-\d{4}-\d{4}-\d{3}[\dX]', profile['orcid']):
                raise ValueError('Use a hyphenated ORCID iD')
        with self.db:
            self.db.execute('UPDATE actors SET profile=? WHERE id=?', (json.dumps(profile),PERSON))
        return self.actor()

    def create_bot(self, fields):
        if set(fields) != {'display_name','bio','scopes'}:
            raise ValueError('Supply display_name, bio and scopes')
        if not isinstance(fields['display_name'],str) or not 1 <= len(fields['display_name'].strip()) <= 100 or not isinstance(fields['bio'],str) or len(fields['bio']) > 2000:
            raise ValueError('Supply a bot name and a description of up to 2000 characters')
        scopes = fields['scopes']
        if not isinstance(scopes,list) or not scopes or any(scope not in {'proposals','feedback','reactions'} for scope in scopes):
            raise ValueError('Bot scopes are proposals, feedback and reactions')
        bid, tid, token = str(uuid.uuid4()), str(uuid.uuid4()), 'nla_bot_' + secrets.token_urlsafe(32)
        profile = {'display_name': fields['display_name'].strip(), 'bio': fields['bio'].strip()}
        with self.db:
            self.db.execute('INSERT INTO actors VALUES(?,?,?,?,?)', (bid,'bot',PERSON,json.dumps(profile),now()))
            self.db.execute('INSERT INTO bot_tokens VALUES(?,?,?,?,NULL)', (tid,bid,hashlib.sha256(token.encode()).hexdigest(),json.dumps(sorted(set(scopes)))))
        return {'bot': self.actor(bid), 'token_id': tid, 'token': token, 'scopes': scopes}

    def bots(self):
        return [{'bot': self.actor(row['bot_id']), 'token_id': row['id'], 'scopes': json.loads(row['scopes']), 'revoked': bool(row['revoked_at'])}
                for row in self.db.execute('SELECT * FROM bot_tokens WHERE bot_id IN (SELECT id FROM actors WHERE owner_id=?)', (PERSON,))]

    def revoke_bot(self, token_id):
        with self.db:
            cursor = self.db.execute('UPDATE bot_tokens SET revoked_at=? WHERE id=? AND bot_id IN (SELECT id FROM actors WHERE owner_id=?)', (now(),token_id,PERSON))
        if not cursor.rowcount:
            raise KeyError('Unknown bot token')
        return {'revoked': True}

    def authenticate_bot(self, token):
        row = self.db.execute('SELECT * FROM bot_tokens WHERE token_hash=? AND revoked_at IS NULL', (hashlib.sha256(token.encode()).hexdigest(),)).fetchone()
        if row is None:
            return None
        return {'actor': self.actor(row['bot_id']), 'scopes': json.loads(row['scopes'])}

    def credit(self, kind, target, oid, actor_id=PERSON, notify=True):
        actor = self.actor(actor_id)
        person = actor['owner_id'] if actor['kind'] == 'bot' else actor['id']
        self.db.execute('INSERT INTO attribution VALUES(?,?,?,?,?,?)', (kind,target,oid,actor_id,person,now()))
        if notify:
            recipients = {row[0] for row in self.db.execute('SELECT person_id FROM subscriptions WHERE object_id=?', (oid,))}
            recipients.discard(person)
            for recipient in recipients:
                self.db.execute('INSERT INTO notifications VALUES(?,?,?,?,?,?,?,NULL)', (str(uuid.uuid4()),recipient,actor_id,oid,kind,target,now()))
            self.db.execute('INSERT OR IGNORE INTO subscriptions VALUES(?,?)', (person,oid))

    def attribution(self, kind, target):
        row = self.db.execute('SELECT actor_id,responsible_person_id FROM attribution WHERE kind=? AND target=?', (kind,target)).fetchone()
        if row is None:
            return None
        return {'actor': self.actor(row['actor_id']), 'responsible_person': self.actor(row['responsible_person_id'])}

    def profile(self, actor_id, cursor=0):
        actor = self.actor(actor_id)
        column = 'responsible_person_id' if actor['kind'] == 'person' else 'actor_id'
        rows = list(self.db.execute(f'SELECT * FROM attribution WHERE {column}=? ORDER BY rowid DESC LIMIT 51 OFFSET ?', (actor_id,cursor)))
        activities=[]
        for row in rows[:50]:
            obj = self.catalog.objects.get(row['object_id'])
            if not obj:
                continue
            url = self.catalog.explorer.statement_url(obj['id']) if obj['type']=='statement' else self.catalog.pages[obj['id']].url
            detail_table = 'feedback' if row['kind']=='comment' else 'revisions'
            detail_column = 'body' if row['kind']=='comment' else 'explanation'
            detail = self.db.execute(f'SELECT {detail_column} FROM {detail_table} WHERE id=?',(row['target'],)).fetchone()
            if row['kind']=='revision':
                url += '?editor-object=' + obj['id'] + '&revision=' + row['target']
            activities.append({**dict(row), 'title': obj['title'], 'url': url, 'excerpt': detail[0][:500] if detail else '', 'excerpt_html': markdown(detail[0][:500]) if detail else '', **self.attribution(row['kind'],row['target'])})
        bots = [self.actor(row[0]) for row in self.db.execute('SELECT id FROM actors WHERE owner_id=? ORDER BY created_at', (actor_id,))]
        reaction_rows = self.db.execute('SELECT r.* FROM actor_reactions r JOIN actors a ON a.id=r.actor_id WHERE a.id=? OR a.owner_id=? ORDER BY r.rowid DESC', (actor_id,actor_id))
        reactions=[]
        for row in reaction_rows:
            obj=self.catalog.objects.get(row['object_id'])
            if obj:
                url=self.catalog.explorer.statement_url(obj['id']) if obj['type']=='statement' else self.catalog.pages[obj['id']].url
                reactions.append({'emoji':row['emoji'],'title':obj['title'],'url':url,'actor':self.actor(row['actor_id'])})
        return {'profile': actor, 'activities': activities, 'bots': bots, 'reactions':reactions, 'next_cursor': cursor+50 if len(rows)>50 else None}

    def follow(self, oid, active):
        self.get(oid)
        if not isinstance(active,bool):
            raise ValueError('Supply an explicit active boolean')
        with self.db:
            if active:
                self.db.execute('INSERT OR IGNORE INTO subscriptions VALUES(?,?)', (PERSON,oid))
            else:
                self.db.execute('DELETE FROM subscriptions WHERE person_id=? AND object_id=?', (PERSON,oid))
        return {'following': active}

    def inbox(self, cursor=0):
        rows = list(self.db.execute('SELECT * FROM notifications WHERE person_id=? ORDER BY rowid DESC LIMIT 51 OFFSET ?', (PERSON,cursor)))
        items=[]
        for row in rows[:50]:
            obj=self.catalog.objects.get(row['object_id'])
            if not obj:
                continue
            url=self.catalog.explorer.statement_url(obj['id']) if obj['type']=='statement' else self.catalog.pages[obj['id']].url
            items.append({**dict(row),'actor':self.actor(row['actor_id']),'title':obj['title'],'url':url})
        return {'items':items,'next_cursor':cursor+50 if len(rows)>50 else None,
                'unread':self.db.execute('SELECT count(*) FROM notifications WHERE person_id=? AND read_at IS NULL',(PERSON,)).fetchone()[0]}
