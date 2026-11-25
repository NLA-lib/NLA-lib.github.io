"""Recovery must reuse data and must not delete a live or unrelated stack."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
TABLE='nla-lib-auth-Data-TFOFBP4JELM9'
STACK='arn:aws:cloudformation:us-west-2:432197736886:stack/nla-lib-auth/15592920-e8b7-11f1-aff0-0affcd16f033'
MOCK_AWS='''#!/usr/bin/env python3
import json,os,sys
args=sys.argv[1:]
with open(os.environ['NLA_TEST_CALLS'],'a') as out:out.write(json.dumps(args)+'\\n')
mode=os.environ.get('NLA_TEST_MODE','')
service,operation=args[:2]
if service=='sts':print('999999999999' if mode=='wrong-account' else '432197736886')
elif service=='dynamodb':print(json.dumps(['ACTIVE',[{'AttributeName':'pk','KeyType':'HASH'},{'AttributeName':'sk','KeyType':'RANGE'}],[{'AttributeName':'pk','AttributeType':'S'},{'AttributeName':'sk','AttributeType':'S'}]]))
elif service=='cloudformation' and operation=='describe-stacks':print('CREATE_COMPLETE' if mode=='live-stack' else 'DELETE_COMPLETE' if mode=='already-deleted' else 'ROLLBACK_COMPLETE')
elif service=='cloudformation' and operation=='describe-stack-resource':print(('wrong-table' if mode=='wrong-table' else 'nla-lib-auth-Data-TFOFBP4JELM9')+'\\tDELETE_SKIPPED')
elif service=='secretsmanager':print('arn:secret')
elif service=='acm':print('ISSUED' if 'Certificate.Status' in args else 'api.nla-lib.org')
elif service=='s3api' and operation=='get-bucket-tagging':print('nla-lib-auth')
'''

class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        (self.root/'bin').mkdir();aws=self.root/'bin/aws';aws.write_text(MOCK_AWS);aws.chmod(0o755)
        (self.root/'auth.zip').write_bytes(b'test-artifact');digest=hashlib.sha256(b'test-artifact').hexdigest();(self.root/'auth.zip.sha256').write_text(digest+'  auth.zip\n')
        self.calls=self.root/'calls.jsonl';self.env={**os.environ,'PATH':str(self.root/'bin')+':'+os.environ['PATH'],'NLA_TEST_CALLS':str(self.calls)}
        self.env.pop('NLA_EXISTING_TABLE',None)
    def execute(self,script,mode=''):
        self.env['NLA_TEST_MODE']=mode
        return subprocess.run(['bash',str(self.root/script)],env=self.env,capture_output=True,text=True)
    def recorded(self):return [json.loads(line) for line in self.calls.read_text().splitlines()]
    def setup_recovery(self):
        shutil.copyfile(ROOT/'recover.sh',self.root/'recover.sh')
        (self.root/'deploy.sh').write_text('set -eu\nprintf "%s" "$NLA_EXISTING_TABLE" > deployed-table\n')
    def test_failed_stack_is_removed_by_exact_id_and_table_is_reused(self):
        self.setup_recovery();result=self.execute('recover.sh');self.assertEqual(result.returncode,0,result.stderr)
        deletions=[call for call in self.recorded() if call[:2]==['cloudformation','delete-stack']]
        self.assertEqual(len(deletions),1);self.assertIn(STACK,deletions[0]);self.assertFalse(any('delete-table' in call for call in self.recorded()))
        self.assertEqual((self.root/'deployed-table').read_text(),TABLE)
        self.assertEqual((self.root/'.existing-data-table').read_text().strip(),TABLE)
    def test_live_stack_wrong_account_and_wrong_table_are_not_deleted(self):
        for mode in ['live-stack','wrong-account','wrong-table']:
            with self.subTest(mode=mode):
                self.setup_recovery();result=self.execute('recover.sh',mode);self.assertNotEqual(result.returncode,0)
                self.assertFalse(any(call[:2]==['cloudformation','delete-stack'] for call in self.recorded()))
                self.assertFalse((self.root/'deployed-table').exists())
    def test_already_deleted_original_stack_skips_deletion(self):
        self.setup_recovery();result=self.execute('recover.sh','already-deleted');self.assertEqual(result.returncode,0,result.stderr)
        self.assertFalse(any(call[:2]==['cloudformation','delete-stack'] for call in self.recorded()))
        self.assertEqual((self.root/'deployed-table').read_text(),TABLE)
    def test_deploy_forwards_retained_table_marker(self):
        shutil.copyfile(ROOT/'deploy.sh',self.root/'deploy.sh');(self.root/'.existing-data-table').write_text(TABLE+'\n')
        result=self.execute('deploy.sh');self.assertEqual(result.returncode,0,result.stderr)
        deploy=next(call for call in self.recorded() if call[:2]==['cloudformation','deploy'])
        self.assertIn('ExistingDataTableName='+TABLE,deploy)
    def test_updates_without_marker_do_not_reset_existing_table_parameter(self):
        shutil.copyfile(ROOT/'deploy.sh',self.root/'deploy.sh');result=self.execute('deploy.sh');self.assertEqual(result.returncode,0,result.stderr)
        deploy=next(call for call in self.recorded() if call[:2]==['cloudformation','deploy'])
        self.assertFalse(any(arg.startswith('ExistingDataTableName=') for arg in deploy))

if __name__=='__main__':unittest.main()
