from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
import time

# Setup Chrome options
options = Options()
options.headless = True
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)
waits = WebDriverWait(driver, 10)

# Load dataset (example query list for testing)
# query_te = ['DAEWOO-SBS-DS-3020MW', 'SNOWA-SBS-S1Di-M210-S']
models_data = []
models_data_torob = []

model_id = 1
common_headers = None  # To store headers from the first query
common_headers_torob = None
header_index_map = {}  # To map headers to their indices
# Load dataset
models = pd.read_excel('model_code.xlsx')
sbs_code_model = models[models['گروه محصول'] == 'ساید بای ساید']
query = sbs_code_model['کد مدل']
first_not_found_index = None
# Process each query
for i, qu in enumerate(query):
    print(f"Processing query {i+1}: {qu}")
    driver.get("https://www.google.com")
    
    # Search for the product model
    search_box = waits.until(EC.element_to_be_clickable((By.NAME, 'q')))
    search_box.send_keys(qu + Keys.ENTER)

    # Wait for search results to load with retry logic
    max_retries = 3
    retry_count = 0
    search_results = None
    
    while retry_count < max_retries:
        try:
            search_results = waits.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.tF2Cxc')))
            break
        except TimeoutException:
            retry_count += 1
            print(f"Timeout while waiting for search results for query: {qu} (Attempt {retry_count}/{max_retries})")
            if retry_count == max_retries:
                print(f"Max retries reached for {qu}, skipping to next query.")
                break
            time.sleep(2)

    if search_results is None:
        continue

    found = False
    found_torob = False
    count_torob = 0
    for result in search_results:
        try:
            link = result.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            if 'digikala.com' in link:
                found = True
                # print(f"Found Digikala link for {qu}: {link}")
                driver.get(link)
                try:
                    price_no_discount = waits.until(EC.element_to_be_clickable((By.XPATH,'//span[@data-testid:"price-no-discount"]'))).text
                except:
                    price_no_discount =None
                    print("Element not found, continuing execution...")
                # Click on feature sections
                featurs_1 = waits.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[1]/div[3]/div[3]/div[2]/div[2]/div[2]/div[2]/div[2]/div[1]/div[3]/button')))
                featurs_1.click()
                featurs_2 = waits.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[1]/div[3]/div[3]/div[2]/div[5]/div[2]/div/section/span')))
                featurs_2.click()

                # Scroll down to load all elements
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                headers = waits.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'styles_SpecificationAttribute__value__CQ4Rz')))
                values = waits.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.styles_SpecificationAttribute__valuesBox__gvZeQ div.grow p.break-words:first-of-type')))

                # Create a dictionary for the model with values aligned to common headers
                model_dict = {'id': model_id, 'model_code': qu, 'price':price_no_discount}
                    
                # Add all header-value pairs to the model dictionary
                for idx, header in enumerate(headers):
                    th = header.text  # Header
                    v = values[idx].text  # Corresponding value
                    model_dict[th] = v

                models_data.append(model_dict)
                model_id += 1
                break  # Exit loop after finding the first Digikala link
            elif 'torob.com' in link:
                found_torob = True
                driver.get(link)
                if first_not_found_index is None:
                    first_not_found_index = i
                # Scroll down to load all elements
                try:
                    price_no_discount = waits.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.Showcase_buy_box_text__otYW_ Showcase_ellipsis__FxqVh'))).text
                except TimeoutException:
                    # Handle the case where the element isn't found
                    price_no_discount = None  # or any default value you prefer
                    print("Element not found, continuing execution...")
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                headers_torob = waits.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.jsx-d9bfdb7eefd5a6bf div.detail-title')))
                values_torob = waits.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.jsx-d9bfdb7eefd5a6bf div.detail-value')))
                
                # Create a dictionary for the model with all headers and values
                model_dict_torob = {
                    'id': model_id,
                    'model_code': qu,
                    'price':price_no_discount
                }

                # Add all header-value pairs to the model dictionary
                for idx, header in enumerate(headers_torob):
                    th = header.text  # Header
                    v = values_torob[idx].text  # Corresponding value
                    model_dict_torob[th] = v
                   
                        
                models_data_torob.append(model_dict_torob)
                model_id += 1
                break  # Exit loop after finding the first Torob link

        except StaleElementReferenceException:
            print("Stale element reference encountered, retrying...")
            continue
        except Exception as e:
            print(f"Error processing search result: {e}")
            continue
    # if model_id == 5:
    #     break
    
    if not found and not found_torob:
        print(f"No link found for {qu}")
# Convert to DataFrame and save to CSV
models_df = pd.DataFrame(models_data)
models_df.to_csv('models_data_digikala.csv', index=False, encoding='utf-8-sig')
models_df = pd.DataFrame(models_data_torob)
models_df.to_csv('models_data_torob.csv', index=False, encoding='utf-8-sig')
print("Data saved to models_data.csv")
input('Press any key to exit...')