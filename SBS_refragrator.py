from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import time
options = Options()
options.headless = True  # Run Chrome without a UI
options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass bot detection
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)
waits = WebDriverWait(driver,10)
#load dataset
models = pd.read_excel('کد مدل.xlsx')
sbs_code_model = models[models['گروه محصول']== 'ساید بای ساید']
query = sbs_code_model['کد مدل']
models_data = []
model_id = 1  # Start with an ID for the first model
ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
wait_2 = WebDriverWait(driver,20,ignored_exceptions=ignored_exceptions)
for i,qu in enumerate(query):
    print(i)
    driver.get("https://www.google.com")
    
    # Search for the product model
    search_box = waits.until(EC.element_to_be_clickable((By.NAME, 'q')))
    search_box.send_keys(qu + Keys.ENTER)
    
    # Wait for search results to load
    search_results = waits.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.tF2Cxc')))
    
    found = False
    # Inside your for loop where you process search results
for result in search_results:
    try:
        # Attempt to find the link
        link = result.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
        if 'digikala.com' in link:
            print(f"Found Digikala link for {qu}: {link}")
            driver.get(link)

            # Use waits to ensure elements are clickable
            featurs_1 = waits.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[1]/div[3]/div[3]/div[2]/div[2]/div[2]/div[2]/div[2]/div[1]/div[3]/button')))
            featurs_1.click()

            featurs_2 = waits.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[1]/div[3]/div[3]/div[2]/div[5]/div[2]/div/section/span')))
            featurs_2.click()

            # Scroll down to load more elements if necessary
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            # time.sleep(2)  # Allow time for the page to load
            headers = waits.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'styles_SpecificationAttribute__value__CQ4Rz')))
            values = waits.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.styles_SpecificationAttribute__valuesBox__gvZeQ div.grow p.break-words')))

            model_dict = {'id': model_id, 'model_code': qu}
            for i, head in enumerate(headers):
                th = head.text
                v = values[i].text
                model_dict[th] = v
            
            models_data.append(model_dict)
            model_id += 1
            found = True

    except StaleElementReferenceException:
        print("Stale element reference encountered, retrying...")
        continue  # This will retry the current iteration

    except Exception as e:
        print(f"Error processing search result: {e}")

# Continue with the rest of your code...
    
    if not found:
        print(f"No Digikala link found for {qu}")
# Convert models_data to DataFrame and save to CSV
models_df = pd.DataFrame(models_data)
models_df.to_csv('models_data.csv', index=False, encoding='utf-8-sig')  # Save as CSV

print("Data saved to models_data.csv")
input('press any key ...')