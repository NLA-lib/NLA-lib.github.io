"""Bounded DynamoDB queries and optimistic multi-record transactions.

Bodies are JSON strings so counters and timestamps keep Python's native types.
No table scans, indexes, or additional AWS resources are needed.
"""
import json
import time
from botocore.exceptions import ClientError


class Conflict(ValueError):
    pass


class Documents:
    def __init__(self, table):
        self.table = table

    def get(self, pk, sk):
        row = self.table.get_item(Key={'pk': pk, 'sk': sk}, ConsistentRead=True).get('Item')
        return ({**json.loads(row['body']), '_version': int(row['version'])} if row and 'body' in row else None)

    def many(self, keys):
        rows = {}
        for offset in range(0, len(keys), 100):
            pending = {self.table.name: {'Keys': [{'pk': pk, 'sk': sk} for pk, sk in keys[offset:offset+100]], 'ConsistentRead': True}}
            for attempt in range(4):
                result = self.table.meta.client.batch_get_item(RequestItems=pending)
                for row in result.get('Responses', {}).get(self.table.name, []):
                    rows[(row['pk'], row['sk'])] = {**json.loads(row['body']), '_version': int(row['version'])}
                pending = result.get('UnprocessedKeys', {})
                if not pending:
                    break
                time.sleep(0.05 * 2**attempt)
            if pending:
                raise RuntimeError('Some activity records could not be loaded; retry')
        return rows

    def query(self, pk, prefix, limit=100, cursor=None, reverse=False):
        args = dict(KeyConditionExpression='pk=:pk AND begins_with(sk,:prefix)',
                    ExpressionAttributeValues={':pk': pk, ':prefix': prefix},
                    Limit=limit, ScanIndexForward=not reverse, ConsistentRead=True)
        if cursor:
            args['ExclusiveStartKey'] = {'pk': pk, 'sk': cursor}
        result = self.table.query(**args)
        return [json.loads(row['body']) for row in result['Items']], result.get('LastEvaluatedKey', {}).get('sk')

    def commit(self, changes):
        transactions = []
        for pk, sk, value, expected in changes:
            condition = 'attribute_not_exists(pk)' if expected is None else '#v=:expected'
            part = {'TableName': self.table.name, 'ConditionExpression': condition}
            if expected is not None:
                part.update(ExpressionAttributeNames={'#v': 'version'},
                            ExpressionAttributeValues={':expected': expected})
            if value is None:
                part['Key'] = {'pk': pk, 'sk': sk}
                transactions.append({'Delete': part})
            else:
                body = {k: v for k, v in value.items() if k != '_version'}
                part['Item'] = {'pk': pk, 'sk': sk, 'version': (expected or 0)+1,
                    'body': json.dumps(body, ensure_ascii=False, separators=(',', ':'))}
                transactions.append({'Put': part})
        try:
            self.table.meta.client.transact_write_items(TransactItems=transactions)
        except ClientError as error:
            if error.response['Error']['Code'] in {'TransactionCanceledException', 'ConditionalCheckFailedException'}:
                reasons = error.response.get('CancellationReasons', [])
                if not reasons or any(x.get('Code') in {'ConditionalCheckFailed', 'TransactionConflict'} for x in reasons):
                    raise Conflict('This item changed. Reload and compare before retrying.') from None
            raise
