import pandas as pd
import json

file_path = "c:/Users/agrik/Documents/agrikranti/mahitimarg-astro/src/assets/District_Taluka_Village_Master.xlsx"
out_path = "c:/Users/agrik/Documents/agrikranti/mahitimarg-astro/src/data/villages.json"

print(f"Reading {file_path}...")
df = pd.read_excel(file_path)

# Ensure columns are cleaned
df.columns = [str(col).strip() for col in df.columns]
print("Columns found:", df.columns.tolist())

# Assuming standard column names exist like 'District', 'Taluka', 'Village' or similar
dist_col = 'DistrictNameMR'
tal_col = 'TalukaNameMR'
vil_col = 'VillageNameMR'

print(f"Using columns: District='{dist_col}', Taluka='{tal_col}', Village='{vil_col}'")

# Build hierarchical dictionary
data = {}
for _, row in df.iterrows():
    dist = str(row[dist_col]).strip().upper()
    tal = str(row[tal_col]).strip().upper()
    vil = str(row[vil_col]).strip().upper()
    
    if pd.isna(dist) or dist == 'NAN': continue
    
    if dist not in data:
        data[dist] = {}
        
    if tal not in data[dist]:
        data[dist][tal] = []
        
    if vil not in data[dist][tal]:
        data[dist][tal].append(vil)

print(f"Processed {len(data.keys())} Districts")

# Sort everything alphabetically
sorted_data = {}
for dist in sorted(data.keys()):
    sorted_data[dist] = {}
    for tal in sorted(data[dist].keys()):
         sorted_data[dist][tal] = sorted(data[dist][tal])

with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(sorted_data, f, ensure_ascii=False)

print(f"Saved JSON to {out_path}")
