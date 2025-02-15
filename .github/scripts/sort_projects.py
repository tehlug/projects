import os
import re
import github
from github import Github

def extract_repo_url(text):
    """Extract GitHub repository URL from text."""
    match = re.search(r'https://github.com/([^/\s]+/[^/\s]+)', text)
    if match:
        repo_url = match.group(1)
        # Remove any trailing characters after the repo URL
        repo_url = re.sub(r'["<>لینک]', '', repo_url)
        return repo_url
    return None

def get_stars_count(repo_url, g):
    """Get star count for a GitHub repository."""
    try:
        repo = g.get_repo(repo_url)
        return repo.stargazers_count
    except Exception:
        return 0

def parse_project_blocks(content):
    """Parse project blocks from the markdown content."""
    blocks = re.split(r'(?=<h2 dir="rtl">)', content)
    
    if not blocks[0].strip().startswith('<h2'):
        blocks = blocks[1:]
    
    return blocks

def sort_projects(content):
    """Sort projects by star count."""
    g = Github(os.getenv('GITHUB_TOKEN'))
    
    blocks = parse_project_blocks(content)
    
    project_data = []
    for block in blocks:
        repo_url = extract_repo_url(block)
        stars = 0
        if repo_url:
            stars = get_stars_count(repo_url, g)
            print(f"Repo: {repo_url}, Stars: {stars}")
        project_data.append((block, stars))
    
    # Sort blocks by star count
    sorted_blocks = sorted(project_data, key=lambda x: x[1], reverse=True)
    
    # Reconstruct the content
    header = "# پروژه‌ها\n\nاین مخزن با هدف آرشیو پروژه‌های اعضای تهلاگ ایجاد شده است. هدف از این مجموعه، افزایش دیده‌شدن، حمایت متقابل و تسهیل همکاری در پروژه‌های یکدیگر است. انتظار می‌رود که این مخزن، تأثیر مثبتی بر فعالیت‌های اعضا در دنیای متن‌باز داشته باشد. برای مشارکت و افزودن پروژه به این لیست، اطلاعات و جزئیات پروژه خود را مطابق با نمونه‌ی اول در یک PR ارسال کنید.\n\n"
    
    sorted_content = header + ''.join(block for block, _ in sorted_blocks)
    
    return sorted_content

def main():
    # Read the current content
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Sort the projects
    sorted_content = sort_projects(content)
    
    # Write the sorted content back
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(sorted_content)
        
    print("Projects sorted successfully!")

if __name__ == '__main__':
    main()