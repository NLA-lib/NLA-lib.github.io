"""The small CloudShell updater preserves collaboration code and original rollback data."""
import hashlib
from pathlib import Path
import runpy
import sys
import tempfile
import unittest
import zipfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from build_auth_return_update import build

class AuthReturnUpdateTests(unittest.TestCase):
    def test_patches_only_auth_sources_and_preserves_the_first_backup(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);helper=build(root/'update.py');module=runpy.run_path(str(helper))
            with zipfile.ZipFile(root/'auth.zip','w') as archive:
                for name,raw in {'app.py':b'OLD APP','store.py':b'OLD STORE','collaboration.py':b'KEEP COMMUNITY','other.txt':b'KEEP OTHER'}.items():archive.writestr(name,raw)
            original=(root/'auth.zip').read_bytes()
            (root/'auth.zip.sha256').write_text(hashlib.sha256(original).hexdigest()+'  auth.zip\n')
            module['apply'](root,deploy=False)
            with zipfile.ZipFile(root/'auth.zip') as archive:
                self.assertEqual(archive.read('collaboration.py'),b'KEEP COMMUNITY')
                self.assertEqual(archive.read('other.txt'),b'KEEP OTHER')
                self.assertIn(b'sign_in_return',archive.read('app.py'))
                self.assertIn(b'return_to',archive.read('store.py'))
            module['apply'](root,deploy=False)
            self.assertEqual((root/'auth.before-signin-return.zip').read_bytes(),original)
            self.assertEqual((root/'auth.zip.sha256').read_text().split()[0],hashlib.sha256((root/'auth.zip').read_bytes()).hexdigest())

    def test_checksum_mismatch_never_changes_archive(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);module=runpy.run_path(str(build(root/'update.py')))
            (root/'auth.zip').write_bytes(b'UNCHANGED');(root/'auth.zip.sha256').write_text('wrong  auth.zip\n')
            with self.assertRaises(RuntimeError):module['apply'](root,deploy=False)
            self.assertEqual((root/'auth.zip').read_bytes(),b'UNCHANGED')

    def test_complete_editor_updater_contains_the_proof_policy_modules(self):
        import base64
        with tempfile.TemporaryDirectory() as tmp:
            module=runpy.run_path(str(build(Path(tmp)/'update.py',('app.py','store.py','content.py','collaboration.py'))))
            self.assertIn('collaboration.py',module['FILES'])
            self.assertIn(b'require_external_proof',base64.b64decode(module['FILES']['content.py']))
            self.assertIn(b'require_external_proof',base64.b64decode(module['FILES']['collaboration.py']))

    def test_editor_updater_adds_new_shared_bibtex_module(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);module=runpy.run_path(str(build(root/'update.py',('app.py','store.py','content.py','collaboration.py','publisher.py','bibtex.py'))))
            with zipfile.ZipFile(root/'auth.zip','w') as archive:
                for name in ['app.py','store.py','content.py','collaboration.py','publisher.py']:archive.writestr(name,b'# old')
                archive.writestr('keep.txt',b'KEEP')
            (root/'auth.zip.sha256').write_text(hashlib.sha256((root/'auth.zip').read_bytes()).hexdigest()+'  auth.zip\n')
            module['apply'](root,deploy=False)
            with zipfile.ZipFile(root/'auth.zip') as archive:
                self.assertIn('bibtex.py',archive.namelist());self.assertEqual(archive.read('keep.txt'),b'KEEP')
