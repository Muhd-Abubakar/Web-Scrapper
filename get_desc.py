import time, random, os, re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
total_desc = []
SAVE_DIR = "Description"
os.makedirs(SAVE_DIR,exist_ok=True)
def extract_number(filename):
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else -1
# Set up Chrome options
chrome_options = uc.ChromeOptions()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument("--headless")  # Run without GUI
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36")
# Launch browser with fallback
driver = None
try:
    driver = uc.Chrome(options=chrome_options, version_main=138)
except Exception as e:
    print(f"Fallback to auto-detection: {e}")
    driver = uc.Chrome(options=chrome_options, use_subprocess=True)
wait = WebDriverWait(driver, 10)
for job_file in sorted(os.listdir("Company_Links"),key=extract_number):
    with open(f"Company_Links/{job_file}", "r", encoding="utf-8") as f:
        job_link = f.read().strip()

    if not job_link:
        print(f"Skipping empty file: {job_file}")
        continue
        
    try:    
        driver.get(job_link)
        time.sleep(random.uniform(3,5))
        desc = wait.until(EC.presence_of_element_located((By.XPATH,'//div[contains(@class, "JobDetails_jobDescription")]')))
        text_content = desc.get_attribute("innerText")
        total_desc.append(text_content)
        time.sleep(random.uniform(1,2))
    except Exception as e:
        print(e)
print(total_desc[1])
for i,des in enumerate(total_desc):
    with open(f'{SAVE_DIR}/description_{i+1}.txt',"w",encoding='utf-8') as f:
        f.write(des)
