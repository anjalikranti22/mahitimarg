import pandas as pd
import json

df = pd.read_excel('District_Taluka_Village_Master.xlsx')
cols = df.columns.tolist()
print("Columns:", cols)

# Find appropriate columns (prioritize Marathi names)
dist_col = next((c for c in cols if 'DistrictNameMR' in c), next((c for c in cols if 'DistrictName' in c), None))
tal_col = next((c for c in cols if 'TalukaNameMR' in c), next((c for c in cols if 'TalukaName' in c), None))
vil_col = next((c for c in cols if 'VillageNameMR' in c), next((c for c in cols if 'VillageName' in c), None))

# fallback
if not dist_col: dist_col = next(c for c in cols if 'District' in c)
if not tal_col: tal_col = next(c for c in cols if 'Taluka' in c)
if not vil_col: vil_col = next(c for c in cols if 'Village' in c)

print(f"Using columns: {dist_col}, {tal_col}, {vil_col}")

res = {}
for _, row in df.iterrows():
    d = str(row[dist_col]).strip()
    t = str(row[tal_col]).strip()
    v = str(row[vil_col]).strip()
    
    if pd.isna(row[dist_col]): continue
    
    if d not in res:
        res[d] = {}
    if t not in res[d]:
        res[d][t] = []
    if v not in res[d][t]:
        res[d][t].append(v)

for d in res:
    for t in res[d]:
        res[d][t].sort()
        
# Sort dicts
res = {k: {tk: sorted(res[k][tk]) for tk in sorted(res[k].keys())} for k in sorted(res.keys())}
        
with open('locations.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False)
print("Successfully generated locations.json")
