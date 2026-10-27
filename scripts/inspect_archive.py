from pathlib import Path
import ast,json
root=Path(__file__).resolve().parents[1];index=json.loads((root/'docs/archive-index.json').read_text(encoding='utf8'));checked=0
for row in index:
    p=root/row['path']
    if row['language']=='python':ast.parse(p.read_text(encoding='utf8'),filename=row['path']);checked+=1
print(json.dumps({'python_sources_parsed':checked,'total_archived_sources':len(index),'archived_sources_executed':0}))
