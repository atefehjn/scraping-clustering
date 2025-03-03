from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
import time

options = Options()
options.headless = True
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)
waits = WebDriverWait(driver, 10)

# Load dataset
models = pd.read_excel('کد مدل.xlsx')
sbs_code_model = models[models['گروه محصول'] == 'ساید بای ساید']
query = sbs_code_model['کد مدل']
models_data = []
model_id = 1

for i, qu in enumerate(query):
    print(i)
    driver.get("https://www.google.com")
    
    # Search for the product model
    search_box = waits.until(EC.element_to_be_clickable((By.NAME, 'q')))
    search_box.send_keys(qu + Keys.ENTER)

    # Wait for search results to load with error handling
    try:
        search_results = waits.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.tF2Cxc')))
    except TimeoutException:
        print(f"Timeout while waiting for search results for query: {qu}")
        continue  # Skip to the next query

    found = False
    for result in search_results:
        try:
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

    if not found:
        print(f"No Digikala link found for {qu}")

# Convert models_data to DataFrame and save to CSV
models_df = pd.DataFrame(models_data)
models_df.to_csv('models_data.csv', index=False, encoding='utf-8-sig')  # Save as CSV

print("Data saved to models_data.csv")
input('press any key ...')