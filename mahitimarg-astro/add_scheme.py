import os
import re

def create_scheme_file():
    print("Welcome to the Scheme Auto-Generator for MahitiMarg (Astro Version)!")
    print("-----------------------------------------------------------------")
    
    title = input("Enter the title of the scheme: ")
    description = input("Enter a short description: ")
    badge = input("Enter the badge (e.g., Farmer, Business, Student): ")
    apply_link = input("Enter the application link: ")
    
    # Generate a slug from the title (basic cleanup)
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', title.lower()).strip('-')
    if not slug:
        slug = "new-scheme"
        
    custom_slug = input(f"Enter a filename/slug (press Enter to use '{slug}'): ")
    if custom_slug.strip():
        slug = custom_slug.strip()
        if not slug.endswith('.md'):
            slug = slug

    print("\nPlease enter/paste the body of your scheme below (Press Enter, then Ctrl+Z on Windows and Enter again to finish saving):")
    
    content_lines = []
    try:
        while True:
            line = input()
            content_lines.append(line)
    except EOFError:
        pass
        
    content = "\n".join(content_lines)

    md_content = f"""---
title: {title}
description: {description}
badge: {badge}
apply_link: {apply_link}
---

# {title}

{content}
"""

    # Make sure we're saving to the correct directory relative to the script
    schemes_dir = os.path.join(os.path.dirname(__file__), 'src', 'content', 'schemes')
    os.makedirs(schemes_dir, exist_ok=True)
    
    filepath = os.path.join(schemes_dir, f"{slug}.md")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(md_content)
        
    print(f"\n✅ Success! The scheme file has been generated and saved to: {filepath}")
    print("Because you are using Astro, this new scheme will automatically show up on your website!")

if __name__ == "__main__":
    create_scheme_file()
