"""Build a standalone CloudShell updater for authentication and editor modules."""
import base64
from pathlib import Path

ROOT=Path(__file__).resolve().parent
TEMPLATE='''#!/usr/bin/env python3
"""Update editor and sign-in code without changing stored users or contributions."""
import base64
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile

FILES=REPLACEMENTS

def apply(root,deploy=True):
    archive=root/'auth.zip';manifest=root/'auth.zip.sha256'
    expected=manifest.read_text().split()[0]
    if hashlib.sha256(archive.read_bytes()).hexdigest()!=expected:
        raise RuntimeError('The package checksum differs. Nothing was changed.')
    replacements={name:base64.b64decode(value) for name,value in FILES.items()}
    for name,raw in replacements.items():compile(raw,name,'exec')
    with zipfile.ZipFile(archive) as old:
        if not {'app.py','store.py','collaboration.py'} <= set(old.namelist()):
            raise RuntimeError('Use the existing collaboration setup directory.')
        backup=root/'auth.before-signin-return.zip'
        if not backup.exists():
            shutil.copyfile(archive,backup)
            shutil.copyfile(manifest,root/'auth.before-signin-return.zip.sha256')
        fd,temporary=tempfile.mkstemp(prefix='signin-return-',suffix='.zip',dir=root)
        os.close(fd)
        try:
            with zipfile.ZipFile(temporary,'w') as updated:
                for info in old.infolist():
                    updated.writestr(info,replacements[info.filename] if info.filename in replacements else old.read(info))
                for name,raw in replacements.items():
                    if name not in old.namelist():updated.writestr(name,raw)
            with zipfile.ZipFile(temporary) as updated:
                if updated.testzip():raise RuntimeError('Package integrity check failed.')
            os.replace(temporary,archive)
        finally:
            if Path(temporary).exists():Path(temporary).unlink()
    manifest.write_text(hashlib.sha256(archive.read_bytes()).hexdigest()+'  auth.zip\\n')
    print('Editor and sign-in code updated. The original package was preserved.',flush=True)
    if deploy:
        subprocess.run(['bash',str(root/'deploy.sh')],check=True)
        print('Deployment complete. Reload the Explorer; proof requirements and sign-in navigation are active.',flush=True)

if __name__=='__main__':
    apply(Path.home()/'nla-lib-collaboration-setup')
'''

def build(output, modules=('app.py','store.py')):
    replacements={name:base64.b64encode(((ROOT/name) if (ROOT/name).is_file() else (ROOT.parent/name)).read_bytes()).decode() for name in modules}
    output=Path(output);output.write_text(TEMPLATE.replace('REPLACEMENTS',repr(replacements)))
    return output

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=Path,required=True);parser.add_argument('--editor',action='store_true')
    args=parser.parse_args();build(args.out,('app.py','store.py','content.py','collaboration.py','publisher.py','bibtex.py','notation.py') if args.editor else ('app.py','store.py'))
