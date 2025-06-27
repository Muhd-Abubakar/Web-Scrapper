import os
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

# Configuration
NUM_CLICKS = 30
SAVE_DIR = 'demo_data'
os.makedirs(SAVE_DIR, exist_ok=True)

# Target URLs
url = {
    "Glassdoor": "https://www.glassdoor.co.in/Job/remote-software-engineer-jobs-SRCH_IL.0,6_IS12563_KO7,24.htm",
}

# Set up Chrome options
chrome_options = uc.ChromeOptions()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--headless")  # Run without GUI
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36")

# Launch browser with fallback
driver = None
try:
    driver = uc.Chrome(options=chrome_options, version_main=138)
except Exception as e:
    print(f"Fallback to auto-detection: {e}")
    driver = uc.Chrome(options=chrome_options, use_subprocess=True)

wait = WebDriverWait(driver, 15)

try:
    print("🔗 Opening Glassdoor...")
    driver.get(url["Glassdoor"])
    time.sleep(10)

    # Try to close login modal if it appears
    try:
        close_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'e1jbctw80')))
        close_button.click()
        print("✖️ Login modal closed.")
    except:
        print("ℹ️ No login modal detected.")

    for i in range(NUM_CLICKS):
        print(f"🔁 Attempt {i+1} to click 'Load More'")
        try:
            button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-test="load-more"]')))
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(random.uniform(3, 6))  # Anti-bot delay
            prev_count = len(driver.find_elements(By.XPATH, '//li[@data-test="jobListing"]'))
            button.click()
            print(f"✅ Clicked 'Load More' {i+1} times")

            # Wait for new jobs to load
            for _ in range(2):
                new_count = len(driver.find_elements(By.XPATH, '//li[@data-test="jobListing"]'))
                if new_count > prev_count:
                    break
                time.sleep(random.uniform(2.5, 3.5))
            else:
                print(f"⚠️ Jobs did not load after click #{i+1}")
                break

        except Exception as e:
            print(f"⚠️ Exception during Load More: {e}")
            break

    print("🔍 Collecting job cards...")
    try:
        job_cards = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//li[@data-test="jobListing"]')))
        print(f"✅ Found {len(job_cards)} job cards.")
        for idx, card in enumerate(job_cards, start=1):
            with open(f"{SAVE_DIR}/JobCard_{idx}.html", "w", encoding="utf-8") as f:
                f.write(card.get_attribute("outerHTML"))
        print(f"✅ All job cards saved to '{SAVE_DIR}'")
    except Exception as e:
        print(f"⚠️ Error finding job cards: {e}")

finally:
    if driver:
        try:
            driver.close()
            driver.quit()
        except:
            pass  # Suppress WinError 6 silently
