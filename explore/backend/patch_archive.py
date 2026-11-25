"""Replace app.py in the existing Lambda zip without reinstalling dependencies."""
import hashlib
import os
from pathlib import Path
import shutil
import tempfile
import zipfile

root=Path(__file__).resolve().parent
archive=root/'auth.zip';manifest=root/'auth.zip.sha256';app=root/'app.py'
compile(app.read_text(),'app.py','exec')
with zipfile.ZipFile(archive) as old:
    if old.namelist().count('app.py')!=1 or not {'provider.py','store.py'}<=set(old.namelist()):
        raise ValueError('This is not the expected authentication Lambda package.')
    if not (root/'auth.before-cors.zip').exists():
        shutil.copyfile(archive,root/'auth.before-cors.zip')
        shutil.copyfile(manifest,root/'auth.before-cors.zip.sha256')
    descriptor,path=tempfile.mkstemp(prefix='auth-cors-',suffix='.zip',dir=root);os.close(descriptor)
    try:
        with zipfile.ZipFile(path,'w') as updated:
            for info in old.infolist():
                content=app.read_bytes() if info.filename=='app.py' else old.read(info)
                updated.writestr(info,content)
        with zipfile.ZipFile(path) as updated:
            if updated.testzip() is not None:raise ValueError('Package integrity check failed.')
        os.replace(path,archive)
    finally:
        if Path(path).exists():Path(path).unlink()
manifest.write_text(hashlib.sha256(archive.read_bytes()).hexdigest()+'  auth.zip\n')
print('Updated the preflight handler; original package preserved as auth.before-cors.zip.')
