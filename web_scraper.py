import requests
from bs4 import BeautifulSoup
import re
import time
import json

BASE_URL = "https://catalog.mines.edu"
INDEX_URL = f"{BASE_URL}/coursesaz/"

def get_department_urls():
    print("Fetching index page...")
    res = requests.get(INDEX_URL)
    # If this prints 403 or 404, the URL itself is the problem
    print(f"Status Code: {res.status_code}") 
    
    soup = BeautifulSoup(res.content, 'html.parser')
    links = []

    # Target the main content area by class (common in Mines catalog)
    content_area = soup.find('div', class_='pagebody') or soup.find('div', id='content')
    
    if content_area:
        # Find every link that starts with /coursesaz/ and has a subdirectory
        # e.g., /coursesaz/math/
        for a in content_area.find_all('a', href=True):
            href = a['href']
            if '/coursesaz/' in href and len(href.strip('/').split('/')) > 1:
                full_url = BASE_URL + href if href.startswith('/') else href
                links.append(full_url)
    
    # Final check: If links is still empty, let's just grab ALL links on the page 
    # that fit the pattern as a last resort.
    if not links:
        for a in soup.find_all('a', href=True):
            if '/coursesaz/' in a['href'] and a['href'] != '/coursesaz/':
                links.append(BASE_URL + a['href'] if a['href'].startswith('/') else a['href'])

    # set() removes duplicates, sorted() keeps it alphabetical
    unique_links = sorted(list(set(links)))
    print(f"Found {len(unique_links)} department links.")
    return unique_links

def scrape_department(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    
    course_list = []
    blocks = soup.find_all('div', class_='courseblock')
    
    for block in blocks:
        title_p = block.find('p', class_='courseblocktitle')
        if not title_p: continue
        full_title = title_p.get_text(strip=True)
        
        # Get the full block text. 
        # Using a newline separator helps regex recognize "end of lines" better
        full_text = block.get_text("\n", strip=True)

        # Initialize defaults
        prereqs = "None"
        coreqs = "None"

        # 1. Split the text into two potential zones to prevent overlap
        # We split on 'Corequisite' (case insensitive)
        parts = re.split(r'(?i)Corequisites?:', full_text)
        
        # The part BEFORE 'Corequisite' contains the Prereqs
        pre_zone = parts[0]
        # The part AFTER 'Corequisite' contains the Coreqs (if it exists)
        co_zone = parts[1] if len(parts) > 1 else ""

        # 2. Extract Prerequisite from the pre_zone
        # We look for 'Prerequisite:' and grab until the end of that sentence/line
        pre_match = re.search(r'(?i)Prerequisites?:\s*(.*)', pre_zone)
        if pre_match:
            prereqs = pre_match.group(1).split('\n')[0].strip()
            # If the catalog literally says "Prerequisite: None.", keep it as None
            if prereqs.lower().startswith("none"):
                prereqs = "None"

        # 3. Extract Corequisite from the co_zone
        if co_zone:
            # Grab everything until the first newline or period
            coreqs = co_zone.split('\n')[0].strip()
            if coreqs.lower().startswith("none"):
                coreqs = "None"

        # 4. Extract Course Code
        code_match = re.search(r'([A-Z]{3,4}\s?\d{3})', full_title)
        course_code = code_match.group(1).replace(" ", "") if code_match else "N/A"

        course_list.append({
            "code": course_code,
            "name": full_title,
            "prereqs": prereqs,
            "coreqs": coreqs
        })
        
    return course_list

# --- Main Execution ---
all_mines_courses = []
# For testing, we might just want to try the first few
dept_urls = get_department_urls()

print(f"Found {len(dept_urls)} departments. Starting scrape...")

for url in dept_urls: # Testing with first 5 departments
    print(f"Scraping: {url}")
    all_mines_courses.extend(scrape_department(url))
    time.sleep(1) # Be nice to the Mines servers!

print(f"Successfully scraped {len(all_mines_courses)} courses.")

with open('mines_catalog.json', 'w') as f:
    json.dump(all_mines_courses, f, indent=4)
    
print("Files saved: mines_catalog.json")