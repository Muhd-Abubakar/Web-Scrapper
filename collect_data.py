from bs4 import BeautifulSoup
import os, re
import pandas as pd


# Help to sort files by number
def extract_number(file_name):
    match = re.search(r'(\d+)', file_name)
    return int(match.group(1)) if match else 0

#=======================Important Functions===========================#

def extract_titles(soup):
    title_tag = soup.find("a", class_="JobCard_jobTitle__GLyJ1")
    return title_tag.get_text(strip=True) if title_tag else "Not specified"

def extract_company(soup):
    company_tag = soup.find("span", class_="EmployerProfile_compactEmployerName__9MGcV")
    return company_tag.get_text(strip=True) if company_tag else "Not specified"

def extract_job_link(soup):
    # Find the first <a> tag with class "JobCard_jobTitle__GLyJ1"
    tag = soup.find("a", class_="JobCard_jobTitle__GLyJ1")
    return tag['href'] if tag and tag.has_attr('href') else "Not specified"

def extract_job_type(soup):
    tag = soup.find("div", class_="JobCard_location__Ds1fM")
    return tag.get_text(strip=True) if tag else "Not specified"

def extract_salary(soup, text):
    salary_patterns = [
        r'₹[\d,]+(?:\.\d+)?\s*-\s*₹[\d,]+(?:\.\d+)?\s*per\s*(month|year)',
        r'From\s+₹[\d,]+(?:\.\d+)?\s*per\s*(month|year)',
        r'₹[\d,]+(?:\.\d+)?\s*per\s*(month|year)',
    ]
    salaries = []
    for pattern in salary_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        salary_strs = re.findall(r'₹[\d,]+(?:\.\d+)?(?:\s*-\s*₹[\d,]+(?:\.\d+)?|)', text)
        for salary in salary_strs:
            salaries.append(salary.strip())

    if salaries:
        return salaries

    tag = soup.find("div", class_="JobCard_salaryEstimate__QpbTW")
    return [tag.get_text(strip=True)] if tag else ["Not specified"]

def extract_experience(des_text):
    text = des_text.lower()
    patterns = [
        r"(\d+)\+?\s*(?:years|yrs)\s+of\s+.*?experience",
        r"at\s+least\s+(\d+)\s*(?:years|yrs)",
        r"minimum\s+of\s+(\d+)\s*(?:years|yrs)",
        r"(\d+)\s*(?:years|yrs)\s+experience",
        r"experience.*?(\d+)\s*(?:years|yrs)",
        r"(\d+)\s*(?:years|yrs)\s*\(required\)"
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1) + " years"
    return "Not specified"

def extract_location(text):
    patterns = [
        r"\bLocation[:\-]?\s*(Remote|Hybrid|On[-\s]?site|[A-Z][a-z]+(?:, [A-Z]{2})?)",
        r"\b(Remote Work|Work from Home|Remote Position)\b",
        r"\bBased in\s+([A-Z][a-z]+(?:, [A-Z]{2})?)",
        r"\b(?:Headquartered|Located) in\s+([A-Z][a-z]+(?:, [A-Z]{2})?)"
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1) if match.groups() else match.group(0)
    return "Not specified"

def extract_skills(soup, text):
    # 1. Try from HTML first
    snippet_div = soup.find("div", class_="JobCard_jobDescriptionSnippet__l1tnl")
    if snippet_div:
        bold_tags = snippet_div.find_all("b")
        for b in bold_tags:
            if "skills" in b.get_text(strip=True).lower():
                # Get the next sibling (text containing the skills)
                if b.next_sibling:
                    skill_text = b.next_sibling.strip(" :–-")
                    skills = re.split(r",\s*|\s+and\s+", skill_text)
                    return [s.strip() for s in skills if s.strip()]  # remove duplicates

    # 2. Fallback: from plain text
    # Look for 'Skills' section and capture the next 1–5 lines after it
    skills_section = re.search(r"(skills|key skills|technical skills)\s*[:\-–]?\s*\n?(.+?)(?:\n{2,}|$)", text, re.IGNORECASE | re.DOTALL)
    
    if skills_section:
        raw_skills = skills_section.group(2)

        # Split on common separators
        skill_list = re.split(r"\n|,|\t|•|-|\u2022|\s+and\s+", raw_skills)
        skill_list = [s.strip() for s in skill_list if len(s.strip()) > 1 and not s.strip().isdigit()]
        return list(set(skill_list)) if skill_list else []

    return []


def extract_contact_info(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'\+?\d[\d\s\-\(\)]{7,}\d'

    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)

    contact_parts = []
    if emails:
        contact_parts.extend(list(set(emails)))
    if phones:
        contact_parts.extend(list(set(phones)))

    return ", ".join(contact_parts) if contact_parts else ""


#=======================Main Code===========================#

d = {
    'title': [],
    'company': [],
    'job_link': [],
    'experience': [],
    'job_type': [],
    'location': [],
    'skills': [],
    'salary': [],
    'hiring_manager': [],
    'contact_details': []
}

LIMIT = None # or Set to number for limit

main_files = sorted(os.listdir("Main_Data"), key=extract_number)
try:
    os.makedirs("Description", exist_ok=True)
    for i, file in enumerate(main_files):
        job_number = extract_number(file)
        try:
            with open(f"Main_Data/{file}", "r", encoding='utf-8') as f:
                html_doc = f.read()
            with open(f'Description/description_{job_number}.txt', 'r', encoding='utf-8') as f:
                des_text = f.read()
        except FileNotFoundError as e:
            print(f"Skipping missing file: {e}")
            continue

        soup = BeautifulSoup(html_doc, "html.parser")

        title = extract_titles(soup)
        company = extract_company(soup)
        job_link = extract_job_link(soup)
        job_type = extract_job_type(soup)
        salary = extract_salary(soup, des_text)
        experience = extract_experience(des_text)
        location = extract_location(des_text)
        skills = extract_skills(soup,des_text)
        contact_info = extract_contact_info(des_text)

        d['title'].append(title)
        d['company'].append(company)
        d['job_link'].append(job_link)
        d['job_type'].append(job_type)
        d['salary'].append(salary)
        d['experience'].append(experience)
        d['location'].append(location)
        d['skills'].append(skills)
        d["contact_details"].append(contact_info)
        d['hiring_manager'].append("Not Specified")

        print(f"Processed {i+1}/{len(main_files)} files: {file}")
        if LIMIT and i + 1 >= LIMIT:
            print(f"Processed {LIMIT} files, stopping for review.")
            break
except Exception as e:
    print(f"An error occurred: {e}")

df = pd.DataFrame(data=d)
df.columns = [f"{col.upper()}" for col in df.columns]
df.to_csv('Collected_data.csv', index=False, encoding='utf-8')
print("✅ Data collection completed and saved to 'Collected_data.csv'.")
