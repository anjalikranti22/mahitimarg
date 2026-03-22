import os
import re
import json

directory = r"c:\Users\agrik\Documents\mahitimarg-astro\src\content\schemes"

with open('renames.json', 'r') as f:
    renames = json.load(f)

# Rename files in the directory
for filename in os.listdir(directory):
    if not (filename.endswith('.md') or filename.endswith('.mdx')):
        continue
    filepath = os.path.join(directory, filename)
    old_slug = os.path.splitext(filename)[0]
    if old_slug in renames:
        new_slug = renames[old_slug]
        ext = os.path.splitext(filename)[1]
        new_filename = f"{new_slug}{ext}"
        new_filepath = os.path.join(directory, new_filename)
        
        # Avoid FileExistsError if the renaming just changes case, or if the target already exists 
        if old_slug != new_slug:
            if os.path.exists(new_filepath) and new_filepath.lower() != filepath.lower():
                print(f"File {new_filename} already exists, skipping rename of {filename}")
            else:
                os.rename(filepath, new_filepath)
                print(f"Renamed {filename} -> {new_filename}")

# Update references
astro_dir = r"c:\Users\agrik\Documents\mahitimarg-astro"

# Sort keys by length descending to prevent partial replacements
sorted_keys = sorted(renames.keys(), key=len, reverse=True)

# Also rename content/schemes files if they exist there
content_schemes_dir = r"c:\Users\agrik\Documents\mahitimarg-astro\content\schemes"
if os.path.exists(content_schemes_dir):
    for filename in os.listdir(content_schemes_dir):
        if filename.endswith('.md'):
            filepath = os.path.join(content_schemes_dir, filename)
            old_slug = os.path.splitext(filename)[0]
            if old_slug in renames:
                new_slug = renames[old_slug]
                new_filepath = os.path.join(content_schemes_dir, f"{new_slug}.md")
                if not os.path.exists(new_filepath):
                    os.rename(filepath, new_filepath)
                    print(f"Renamed (in content) {filename} -> {new_slug}.md")


# Also rename schemes/*.html if they exist there
html_schemes_dir = r"c:\Users\agrik\Documents\mahitimarg-astro\schemes"
if os.path.exists(html_schemes_dir):
    for filename in os.listdir(html_schemes_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(html_schemes_dir, filename)
            old_slug = os.path.splitext(filename)[0]
            if old_slug in renames:
                new_slug = renames[old_slug]
                new_filepath = os.path.join(html_schemes_dir, f"{new_slug}.html")
                # Sometimes a windows rename fails if it exists
                if filepath.lower() != new_filepath.lower():
                    if os.path.exists(new_filepath):
                        os.remove(new_filepath)
                    os.rename(filepath, new_filepath)
                    print(f"Renamed (html) {filename} -> {new_slug}.html")


for root, dirs, files in os.walk(astro_dir):
    # Avoid node_modules or dist if necessary, though it shouldn't matter too much
    if "node_modules" in root or ".git" in root:
        continue
    for f in files:
        if f.endswith(('.html', '.astro', '.md', '.mdx', '.js', '.ts', '.json')):
            if f == 'renames.json':
                continue
            filepath = os.path.join(root, f)
            try:
                with open(filepath, 'r', encoding='utf-8') as fp:
                    content = fp.read()
                original_content = content
                
                for old_slug in sorted_keys:
                    new_slug = renames[old_slug]
                    # We only replace if it's the old slug surrounded by typical URL boundaries or similar
                    # But a simple replace is usually fine for these specific strings
                    if old_slug in content:
                        content = content.replace(old_slug, new_slug)
                
                if content != original_content:
                    with open(filepath, 'w', encoding='utf-8') as fp:
                        fp.write(content)
                    print(f"Updated references in {filepath}")
            except Exception as e:
                # ignore files that can't be read like binaries
                pass

print("Done updating!")
