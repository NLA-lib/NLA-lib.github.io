#!/usr/bin/env python3
"""Package a previously installed, hash-pinned Lambda runtime; never accesses AWS."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parent

def add(archive,path,name):
    info=zipfile.ZipInfo(name,(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
    info.external_attr=(path.stat().st_mode & 0o777)<<16
    archive.writestr(info,path.read_bytes())

def build(runtime,output):
    output.mkdir(parents=True,exist_ok=True)
    code=output/'auth.zip'
    with zipfile.ZipFile(code,'w') as archive:
        for file in sorted(runtime.rglob('*')):
            if file.is_file() and '__pycache__' not in file.parts and file.suffix!='.pyc' and not file.relative_to(runtime).parts[0]=='bin':
                add(archive,file,file.relative_to(runtime).as_posix())
        for name in ['app.py','store.py','provider.py','account.js','account.css','collaboration.py','content.py','documents.py','publisher.py']:
            add(archive,ROOT/name,name)
        for name in ['notation.py','notation.json']:
            add(archive,ROOT.parent/name,name)
    with zipfile.ZipFile(code) as archive:
        if sum(info.file_size for info in archive.infolist())>250*1024*1024:
            raise ValueError('Lambda package exceeds the uncompressed deployment limit')
    digest=hashlib.sha256(code.read_bytes()).hexdigest()
    (output/'auth.zip.sha256').write_text(digest+'  auth.zip\n')
    bundle=output/'nla-lib-auth-setup.zip'
    with zipfile.ZipFile(bundle,'w') as archive:
        for name in ['README.md','COLLABORATION.md','template.yaml','deploy.sh','recover.sh','bootstrap-admin.sh','requirements.in','requirements.lock']:
            add(archive,ROOT/name,name)
        for name in ['auth.zip','auth.zip.sha256']:
            add(archive,output/name,name)
    collaboration_bundle=output/'nla-lib-collaboration-setup.zip'
    collaboration_bundle.write_bytes(bundle.read_bytes())
    recovery=output/'nla-lib-auth-recovery.zip'
    with zipfile.ZipFile(recovery,'w') as archive:
        for name in ['README.md','template.yaml','deploy.sh','recover.sh']:
            add(archive,ROOT/name,name)
    browser_fix=output/'nla-lib-auth-browser-fix.zip'
    with zipfile.ZipFile(browser_fix,'w') as archive:
        for name in ['app.py','apply-cors-fix.sh','patch_archive.py']:
            add(archive,ROOT/name,name)
    print(json.dumps({'bundle':str(bundle),'bundle_bytes':bundle.stat().st_size,'recovery':str(recovery),'browser_fix':str(browser_fix),'lambda_sha256':digest}))
    return bundle

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--runtime',type=Path,required=True);parser.add_argument('--out',type=Path,required=True);args=parser.parse_args();build(args.runtime,args.out)
