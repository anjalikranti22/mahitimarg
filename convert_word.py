import os
import mammoth
import re
import subprocess

# Define paths
BASE_DIR = r'c:\Users\agrik\Documents\agrikranti'
WORD_DIR = os.path.join(BASE_DIR, 'content', 'word_docs')
MD_DIR = os.path.join(BASE_DIR, 'content', 'schemes')

# Ensure directories exist
os.makedirs(WORD_DIR, exist_ok=True)
os.makedirs(MD_DIR, exist_ok=True)

def generate_filename(title):
    """Converts a title to a url-friendly filename"""
    # Simply convert spaces to hyphens and make lowercase, remove quotes
    clean_name = re.sub(r'[^\w\s-]', '', title.lower())
    return re.sub(r'[-\s]+', '-', clean_name).strip('-')

def convert_word_to_md():
    """Reads all .docx files and converts them to Markdown"""
    
    files_processed = 0

    for filename in os.listdir(WORD_DIR):
        if not filename.endswith('.docx') or filename.startswith('~'):
            continue
            
        filepath = os.path.join(WORD_DIR, filename)
        
        print(f"Reading Word document: {filename}...")
        
        # We need a custom mapping to ensure lists and headers come out clean
        style_map = """
        p[style-name='Heading 1'] => h1:fresh
        p[style-name='Heading 2'] => h2:fresh
        """
        
        with open(filepath, "rb") as docx_file:
            # Mammoth converts directly to Markdown
            result = mammoth.convert_to_markdown(docx_file, style_map=style_map)
            markdown_text = result.value
            messages = result.messages
            
            if messages:
                print(f"Warnings converting {filename}:", messages)
                
        # Try to extract a title from the filename (e.g., "Mazi Kanya Bhagyashree.docx")
        clean_title = filename.replace('.docx', '').strip()
        url_name = generate_filename(clean_title)
        
        # Create Frontmatter for our site builder
        frontmatter = f"""---
title: {clean_title}
description: महाराष्ट्र शासनाची योजना.
badge: New Scheme
apply_link: https://sjsa.maharashtra.gov.in/
---

"""
        # Combine frontmatter and mammoth markdown output
        final_markdown = frontmatter + markdown_text
        
        # Save as a .md file in the content/schemes folder
        md_output_path = os.path.join(MD_DIR, f"{url_name}.md")
        with open(md_output_path, 'w', encoding='utf-8') as f:
            f.write(final_markdown)
            
        print(f"✅ Converted {filename} -> {url_name}.md")
        files_processed += 1
        
        # Optional: Delete the word doc after converting so we don't process it twice
        # os.remove(filepath) 

    if files_processed == 0:
        print(f"No Word (.docx) files found in {WORD_DIR}. Please add some!")
    else:
        print(f"\nSuccessfully converted {files_processed} Word documents to Markdown!")
        print("Now running the HTML website builder...")
        
        # Automatically run our site generator
        script_path = os.path.join(BASE_DIR, 'generate_scheme.py')
        subprocess.run(["python", script_path], cwd=BASE_DIR)

# Run the converter
if __name__ == "__main__":
    convert_word_to_md()
