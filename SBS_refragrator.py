from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re
import pandas as pd

options = Options()
options.headless = True  # Run Chrome without a UI
options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass bot detection
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")

driver = webdriver.Chrome(options=options)
waits = WebDriverWait(driver,10)
#load dataset
models = pd.read_excel('کد مدل.xlsx')
sbs_code_model = models[models['گروه محصول']== 'ساید بای ساید']
query = sbs_code_model['کد مدل']

for qu in query[:1]:
    driver.get("https://www.google.com")
    
    # Search for the product model
    search_box = waits.until(EC.element_to_be_clickable((By.NAME, 'q')))
    search_box.send_keys(qu + Keys.ENTER)
    
    # Wait for search results to load
    search_results = waits.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.tF2Cxc')))
    
    found = False
    for result in search_results:
        try:
            link = result.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            if 'digikala.com' in link:
                print(f"Found Digikala link for {qu}: {link}")
                driver.get(link)  # Open the Digikala link
                found = True
                featurs_1 = waits.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="__next"]/div[1]/div[3]/div[3]/div[2]/div[2]/div[2]/div[2]/div[2]/div[1]/div[3]/button'))).click()
                featurs_2 = waits.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="__next"]/div[1]/div[3]/div[3]/div[2]/div[5]/div[2]/div/section/span')))
                tables = driver.find_elements(By.TAG_NAME, "table")
                data = {}

        # Loop through each table
        for table in tables:
            rows = table.find_elements(By.TAG_NAME, "tr")
            
            for row in rows:
                # Extract header and value
                header = row.find_element(By.TAG_NAME, "th").text.strip()
                value = row.find_element(By.TAG_NAME, "td").text.strip()
                
                # Store in dictionary
                data[header] = value

            # Convert dictionary to Pandas DataFrame
            df = pd.DataFrame([data])

            # Save to CSV or Excel (optional)
            df.to_csv("fridge_specs.csv", index=False)
            df.to_excel("fridge_specs.xlsx", index=False)
        except Exception as e:
            print(f"Error processing search result: {e}")
    
    if not found:
        print(f"No Digikala link found for {qu}")

input('press any key ...')