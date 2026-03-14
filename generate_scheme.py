import os
import markdown
import frontmatter
import re

# Define paths
BASE_DIR = r'c:\Users\agrik\Documents\agrikranti'
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
INCLUDES_DIR = os.path.join(TEMPLATES_DIR, 'includes')
SCHEMES_DIR = os.path.join(BASE_DIR, 'content', 'schemes') # Where the user puts .md files
OUTPUT_DIR = os.path.join(BASE_DIR, 'schemes') # Where the HTML gets built
INDEX_PATH = os.path.join(BASE_DIR, 'index.html')

# Ensure directories exist
os.makedirs(SCHEMES_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load layout components
try:
    with open(os.path.join(INCLUDES_DIR, 'header.html'), 'r', encoding='utf-8') as f:
        HEADER_HTML = f.read()
    with open(os.path.join(INCLUDES_DIR, 'footer.html'), 'r', encoding='utf-8') as f:
        FOOTER_HTML = f.read()
    with open(os.path.join(INCLUDES_DIR, 'sidebar.html'), 'r', encoding='utf-8') as f:
        SIDEBAR_HTML = f.read()
except FileNotFoundError as e:
    print(f"Error: Could not find template include files: {e}")
    exit(1)

def get_category_icon(category):
    """Returns a tuple of (icon_class, bg_class, emoji) based on category"""
    cat = category.lower()
    if 'farmer' in cat or 'शेतकरी' in cat:
        return ('fa-tractor', 'bg-green', '🧑‍🌾 Farmer')
    if 'women' in cat or 'महिला' in cat:
        return ('fa-person-dress', 'bg-pink', '👩 Women')
    if 'business' in cat or 'व्यवसाय' in cat:
        return ('fa-store', 'bg-orange', '💼 Business')
    if 'student' in cat or 'विद्यार्थी' in cat:
        return ('fa-graduation-cap', 'bg-purple', '🎓 Students')
    return ('fa-leaf', 'bg-blue', '📋 Scheme')

def generate_index_card(data):
    """Generates the HTML for a single scheme card on the homepage"""
    icon_class, bg_class, badge_text = get_category_icon(data.get('badge', ''))
    
    return f"""
                <!-- Scheme Card: {data['title']} -->
                <article class="glass-panel scheme-card animate-on-scroll" data-tags="{data.get('badge', '').lower()}">
                    <div class="scheme-img-wrapper">
                        <div class="scheme-icon-bg {bg_class}">
                            <i class="fa-solid {icon_class}" aria-hidden="true"></i>
                        </div>
                        <div class="badge-group">
                            <span class="badge badge-tag">{badge_text}</span>
                            <span class="badge badge-active">Active</span>
                        </div>
                    </div>
                    <div class="scheme-card-content">
                        <h3>{data['title']}</h3>
                        <p class="scheme-desc">{data['description']}</p>
                    </div>
                    <a href="schemes/{data['filename']}" class="btn btn-primary btn-block btn-read-more ripple-effect">
                        माहिती वाचा <i class="fa-solid fa-arrow-right arrow-icon"></i>
                    </a>
                </article>"""

def update_index_page(scheme_cards_html):
    """Injects the generated scheme cards into index.html"""
    if not os.path.exists(INDEX_PATH):
        print(f"Warning: {INDEX_PATH} not found. Skipping index update.")
        return

    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        index_content = f.read()

    # Find the markers and replace content between them
    start_marker = "<!-- AUTO_SCHEMES_START -->"
    end_marker = "<!-- AUTO_SCHEMES_END -->"
    
    if start_marker in index_content and end_marker in index_content:
        pattern = re.compile(f"{start_marker}.*?{end_marker}", re.DOTALL)
        new_content = pattern.sub(f"{start_marker}{scheme_cards_html}\n                {end_marker}", index_content)
        
        with open(INDEX_PATH, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("✅ Successfully updated index.html with new scheme cards!")
    else:
        print("Error: Could not find AUTO_SCHEMES markers in index.html")

def build_html_from_markdown():
    """Reads all .md files in content/schemes and generates HTML files."""
    
    # Configure Markdown to handle lists, headers, etc. nicely
    md = markdown.Markdown(extensions=['meta', 'sane_lists', 'nl2br'])
    
    files_processed = 0
    all_schemes_data = []

    for filename in sorted(os.listdir(SCHEMES_DIR), reverse=True): # Newest first?
        if not filename.endswith('.md'):
            continue
            
        filepath = os.path.join(SCHEMES_DIR, filename)
        
        # Parse the markdown file (separates YAML frontmatter from content)
        with open(filepath, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
            
        # Get metadata with defaults
        title = post.get('title', 'नवीन योजना')
        description = post.get('description', '')
        badge = post.get('badge', 'Scheme')
        apply_link = post.get('apply_link', '#')
        
        # Save for index update
        all_schemes_data.append({
            'title': title,
            'description': description,
            'badge': badge,
            'filename': filename.replace('.md', '.html')
        })
        
        # Convert markdown text to HTML
        content_html = md.reset().convert(post.content)
        
        # Build the final page
        html_page = f"""<!DOCTYPE html>
<html lang="mr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | MahitiMarg 2026</title>
    <meta name="description" content="{description}">
    
    <link rel="stylesheet" href="../css/styles.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Google tag (gtag.js) Placeholder -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-BEB9SJ3QXK"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-BEB9SJ3QXK');
    </script>
</head>
<body>
{HEADER_HTML}

    <main class="scheme-detail-layout">
        
        <article class="glass-panel scheme-detail-page" style="padding: 2.5rem; background: #fff; border-radius: var(--radius-lg); box-shadow: var(--shadow-soft);">
            <div class="section-badge"><i class="fa-solid fa-leaf"></i> {badge}</div>
            <h1 style="color: var(--primary); margin-bottom: 0.5rem; font-size: 2.2rem;">{title}</h1>
            
            <div class="scheme-content" style="margin-top: 2rem; line-height: 1.8;">
                {content_html}
            </div>
            
            <div style="margin-top: 3rem; padding-top: 2rem; border-top: 1px solid #eee;">
                <h2 style="color: var(--text-dark);"><i class="fa-solid fa-laptop-file text-primary"></i> अर्ज कसा करावा? (How to Apply)</h2>
                <p>या योजनेसाठी तुम्ही अधिकृत पोर्टलवर जाऊन ऑनलाइन अर्ज करू शकता.</p>
                <a href="{apply_link}" class="btn btn-primary" style="margin-top: 15px; display: inline-block;">
                    <i class="fa-solid fa-arrow-up-right-from-square"></i> ऑनलाइन अर्ज करा
                </a>
            </div>

        </article>

{SIDEBAR_HTML}

    </main>

{FOOTER_HTML}
</body>
</html>"""

        # Save the file (.md filename becomes .html filename)
        output_filename = filename.replace('.md', '.html')
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_page)
            
        print(f"Generated: {output_filename}")
        files_processed += 1

    # Now update the home page with cards for all schemes
    scheme_cards_html = ""
    for data in all_schemes_data:
        scheme_cards_html += generate_index_card(data)
    
    update_index_page(scheme_cards_html)

    if files_processed == 0:
        print(f"No .md files found in {SCHEMES_DIR}. Please add some to generate pages!")
    else:
        print(f"\nSuccess! Generated {files_processed} scheme pages and updated index.html.")

# Run the builder
if __name__ == "__main__":
    build_html_from_markdown()
