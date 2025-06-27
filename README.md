# 💼 Talrn Job Listing Web Scraper

This project is a custom-built web scraper developed for an internship task at **Talrn.com**. It automates the extraction of job-related information from saved HTML files, capturing essential fields such as job title, company, salary, experience, contact details, and more.

> 🧠 Designed with real-world job data parsing challenges in mind, the script demonstrates strong web scraping, data cleaning, and regular expression skills.

---

## 🚀 Features

- Extracts job title, company name, job type, and salary  
- Parses free-text job descriptions for:  
  - Required experience  
  - Job location (e.g., Remote, Hybrid)  
  - Skills  
  - Contact details (email, phone)  
- Handles missing or inconsistent data gracefully  
- Saves all structured data to a clean CSV file  
- Organized file input-output with automatic filename matching  

---

## 🛠 Tech Stack

| Technology                | Purpose                                   |
|---------------------------|-------------------------------------------|
| `undetected-chromedriver` | Bypasses anti-bot mechanisms on dynamic pages |
| `selenium`                | Browser automation for scraping           |
| `beautifulsoup4`          | HTML parsing and tag navigation           |
| `pandas`                  | Data structuring and CSV export           |
| `regex` (re module)       | Extracting info from unstructured text    |

---

## 📂 Project Structure

Web-Scrapper/
├── Main\_Data/                  # Saved job listing HTML files
├── Description/                # Plain text job descriptions
├── scraper\_script.py           # Core logic for parsing and extracting data
├── Collected\_data.csv          # Final structured dataset
├── requirements.txt            # Python dependencies
└── .gitignore                  # Ignored folders & system files

---

## 🧪 How to Run

1. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

3. **Place your files**

   * HTML listings → `Main_Data/`
   * Job descriptions → `Description/` (matching filenames)

4. **Run the scraper**

   ```bash
   python scraper_script.py
   ```

5. **View output**

   * `Collected_data.csv` will be generated in the root folder.

---

## 📈 Sample Fields Extracted

| Field             | Description                                 |
| ----------------- | ------------------------------------------- |
| `TITLE`           | Job title from the listing                  |
| `COMPANY`         | Company name                                |
| `JOB_LINK`        | Direct link to job (if available)           |
| `JOB_TYPE`        | Remote, Hybrid, On-site, etc.               |
| `EXPERIENCE`      | Years of experience parsed from description |
| `SALARY`          | Salary estimate (range or fixed)            |
| `LOCATION`        | City/Remote status                          |
| `SKILLS`          | Keywords/technologies mentioned             |
| `CONTACT_DETAILS` | Extracted email or phone number             |
| `HIRING_MANAGER`  | Defaulted to "Not Specified"                |

---

## 💡 Additional Suggestions for Talrn

* Implement structured schema tags in job listings for better parsing and SEO
* Add unique job IDs to avoid duplicate entries
* Introduce category tags (e.g., Python, React, AI) for easier filtering
* Store job posting timestamps in metadata
