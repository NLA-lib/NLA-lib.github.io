"""DynamoDB records for the initial hosted authentication slice."""
import hashlib
import time
import uuid
from botocore.exceptions import ClientError


def fingerprint(value):
    return hashlib.sha256(value.encode()).hexdigest()


class LimitReached(Exception):
    pass


class Store:
    def __init__(self, table, clock=time.time):
        self.table, self.clock = table, clock

    def get(self, pk, sk):
        return self.table.get_item(Key={'pk': pk, 'sk': sk}, ConsistentRead=True).get('Item')

    def limit(self, key, maximum, expires):
        try:
            self.table.update_item(Key={'pk': 'LIMIT#'+key, 'sk': 'LIMIT'},
                UpdateExpression='SET expires_at=if_not_exists(expires_at,:expires) ADD #n :one',
                ConditionExpression='attribute_not_exists(#n) OR #n < :maximum',
                ExpressionAttributeNames={'#n': 'count'},
                ExpressionAttributeValues={':expires': expires, ':one': 1, ':maximum': maximum})
        except ClientError as error:
            if error.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise LimitReached() from None
            raise

    def login_limit(self, address, daily_limit=1000):
        current = int(self.clock())
        self.limit('IP#'+fingerprint(address)+'#'+str(current//3600), 20, current+7200)
        self.limit('DAY#'+str(current//86400), daily_limit, current+172800)

    def create_flow(self, state, browser, return_to='/explore/?auth=complete'):
        self.table.put_item(Item={'pk': 'STATE#'+fingerprint(state), 'sk': 'STATE',
            'browser_hash': fingerprint(browser), 'return_to': return_to, 'expires_at': int(self.clock())+600},
            ConditionExpression='attribute_not_exists(pk)')

    def consume_flow(self, state, browser):
        try:
            result = self.table.delete_item(Key={'pk': 'STATE#'+fingerprint(state), 'sk': 'STATE'},
                ConditionExpression='browser_hash=:browser AND expires_at > :now',
                ExpressionAttributeValues={':browser': fingerprint(browser), ':now': int(self.clock())},
                ReturnValues='ALL_OLD')
            return result.get('Attributes') or False
        except ClientError as error:
            if error.response['Error']['Code'] == 'ConditionalCheckFailedException':
                return False
            raise

    def ensure_person(self, orcid, name):
        person_id = str(uuid.uuid5(uuid.NAMESPACE_URL, 'https://orcid.org/'+orcid))
        key = {'pk': 'PERSON#'+person_id, 'sk': 'PROFILE'}
        person = {**key, 'id': person_id, 'kind': 'person', 'orcid': orcid,
            'display_name': name[:200] or orcid, 'bio': '', 'affiliation': '', 'interests': '',
            'website': '', 'role': 'contributor', 'status': 'active', 'created_at': int(self.clock())}
        try:
            self.table.put_item(Item=person, ConditionExpression='attribute_not_exists(pk)')
            return person
        except ClientError as error:
            if error.response['Error']['Code'] != 'ConditionalCheckFailedException':
                raise
            return self.get(**key)

    def person(self, person_id):
        return self.get('PERSON#'+person_id, 'PROFILE')

    def create_session(self, token, person_id, csrf):
        current = int(self.clock())
        self.table.put_item(Item={'pk': 'SESSION#'+fingerprint(token), 'sk': 'SESSION',
            'person_id': person_id, 'csrf': csrf, 'created_at': current, 'expires_at': current+43200},
            ConditionExpression='attribute_not_exists(pk)')
        self.audit(person_id, 'signed_in')

    def session(self, token):
        if not token:
            return None
        item = self.get('SESSION#'+fingerprint(token), 'SESSION')
        if not item or int(item['expires_at']) <= int(self.clock()):
            return None
        person = self.person(item['person_id'])
        if not person or person.get('status') != 'active':
            return None
        return {'record': item, 'person': person}

    def delete_session(self, token):
        if token:
            self.table.delete_item(Key={'pk': 'SESSION#'+fingerprint(token), 'sk': 'SESSION'})

    def audit(self, person_id, action):
        self.table.put_item(Item={'pk': 'PERSON#'+person_id,
            'sk': 'AUDIT#'+str(int(self.clock()))+'#'+str(uuid.uuid4()),
            'actor_id': person_id, 'responsible_person_id': person_id, 'action': action,
            'created_at': int(self.clock())})

    def update_profile(self, person_id, fields):
        if not fields:
            return self.person(person_id)
        names = {'#status': 'status'}
        values = {':active': 'active'}
        assignments = []
        for index, (key, value) in enumerate(fields.items()):
            names['#f'+str(index)] = key
            values[':v'+str(index)] = value
            assignments.append('#f'+str(index)+'=:v'+str(index))
        result = self.table.update_item(Key={'pk': 'PERSON#'+person_id, 'sk': 'PROFILE'},
            UpdateExpression='SET '+','.join(assignments), ConditionExpression='#status=:active',
            ExpressionAttributeNames=names, ExpressionAttributeValues=values, ReturnValues='ALL_NEW')
        self.audit(person_id, 'profile_updated')
        return result['Attributes']
