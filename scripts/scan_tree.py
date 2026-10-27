"""Read-only bounded directory-size report. No deletion or network access."""
from pathlib import Path
import argparse,json,os
def scan(root,max_files):
    total=0;count=0;skipped=0;truncated=False
    for current,dirs,files in os.walk(root,followlinks=False):
        dirs[:]=sorted(d for d in dirs if not(Path(current)/d).is_symlink() and not(Path(current)/d).is_junction())
        for name in sorted(files):
            p=Path(current)/name
            if p.is_symlink():skipped+=1;continue
            if count>=max_files:truncated=True;break
            try:total+=p.stat().st_size;count+=1
            except OSError:skipped+=1
        if truncated:break
    return dict(bytes=total,files=count,skipped=skipped,truncated=truncated)
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('root',type=Path);parser.add_argument('--max-files',type=int,default=200000);args=parser.parse_args()
    if not args.root.is_dir() or args.max_files<1:parser.error('Provide an existing directory and positive file limit.')
    print(json.dumps(scan(args.root,args.max_files),ensure_ascii=False))
