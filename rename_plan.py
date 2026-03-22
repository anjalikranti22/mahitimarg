import os
import re

directory = r"c:\Users\agrik\Documents\mahitimarg-astro\src\content\schemes"

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')

renames = {}

for filename in os.listdir(directory):
    if not (filename.endswith('.md') or filename.endswith('.mdx')):
        continue
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # match english_title
    match = re.search(r'english_title:\s*\"?([^\n\"]+)\"?', content)
    if not match:
        match = re.search(r'title:\s*\"?([^\n\"]+)\"?', content)
        
    if match:
        title = match.group(1).strip()
        slug = slugify(title)
        ext = os.path.splitext(filename)[1]
        new_filename = f"{slug}{ext}"
        if new_filename != filename:
            old_slug = os.path.splitext(filename)[0]
            renames[old_slug] = slug
            print(f"{filename} -> {new_filename}")

print("\n--- Summary ---")
for k, v in renames.items():
    print(f"{k} -> {v}")

# Write to a JSON file to see it easily
import json
with open('renames.json', 'w') as f:
    json.dump(renames, f, indent=2)
