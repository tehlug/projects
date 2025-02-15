import os
import re

def parse_project_blocks(content):
    """Parse project blocks from the markdown content."""
    blocks = re.split(r'(?=<h2 dir="rtl">)', content)
    
    if not blocks[0].strip().startswith('<h2'):
        blocks = blocks[1:]
    
    return blocks

def format_to_table(blocks):
    """Convert project blocks to markdown table format."""
    # Table header
    table = "| اسم | توضیحات | لینک‌ها |\n|------|----------|----------|\n"
    
    for block in blocks:
        # Extract name
        name_match = re.search(r'<h2 dir="rtl">(.*?)</h2>', block)
        name = name_match.group(1) if name_match else ""
        
        # Extract description
        desc_match = re.search(r'<p dir="rtl">(.*?)</p>', block, re.DOTALL)
        description = desc_match.group(1) if desc_match else ""
        description = description.replace('\n', ' ').strip()
        
        # Extract links
        links = []
        for link_match in re.finditer(r'<a href="(.*?)">(.*?)</a>', block):
            url, text = link_match.groups()
            links.append(f"[{text}]({url})")
        
        links_str = " | ".join(links)
        
        # Add row to table
        table += f"| {name} | {description} | {links_str} |\n"
    
    return table

def main():
    with open('projects.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    header_match = re.match(r'(.*?)(?=<h2 dir="rtl">)', content, re.DOTALL)
    header = header_match.group(1) if header_match else ""
    
    blocks = parse_project_blocks(content)
    table = format_to_table(blocks)
    
    formatted_content = header + "\n" + table
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(formatted_content)
        
    print("Projects formatted to table successfully!")

if __name__ == '__main__':
    main()