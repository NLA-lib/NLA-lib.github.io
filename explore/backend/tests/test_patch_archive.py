import hashlib
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT=Path(__file__).resolve().parents[1]

class PatchTests(unittest.TestCase):
    def test_only_app_changes_and_original_backup_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);shutil.copyfile(ROOT/'patch_archive.py',root/'patch_archive.py');(root/'app.py').write_text('VALUE=2\n')
            with zipfile.ZipFile(root/'auth.zip','w') as archive:
                for name,body in [('app.py',b'VALUE=1\n'),('provider.py',b'provider'),('store.py',b'store'),('package/binary.so',bytes(range(256)))]:archive.writestr(name,body)
            original=(root/'auth.zip').read_bytes();(root/'auth.zip.sha256').write_text(hashlib.sha256(original).hexdigest()+'  auth.zip\n')
            result=subprocess.run([sys.executable,str(root/'patch_archive.py')],capture_output=True,text=True);self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual((root/'auth.before-cors.zip').read_bytes(),original)
            with zipfile.ZipFile(root/'auth.zip') as archive:
                self.assertEqual(archive.read('app.py'),b'VALUE=2\n');self.assertEqual(archive.read('package/binary.so'),bytes(range(256)))
            digest=hashlib.sha256((root/'auth.zip').read_bytes()).hexdigest();self.assertTrue((root/'auth.zip.sha256').read_text().startswith(digest))
            again=subprocess.run([sys.executable,str(root/'patch_archive.py')],capture_output=True,text=True);self.assertEqual(again.returncode,0,again.stderr);self.assertEqual((root/'auth.before-cors.zip').read_bytes(),original)

if __name__=='__main__':unittest.main()
