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
model_id = 1
common_headers = None  # To store headers from the first query
header_index_map = {}  # To map headers to their indices
# Load dataset
models = pd.read_excel('کد مدل.xlsx')
sbs_code_model = models[models['گروه محصول'] == 'ساید بای ساید']
query = sbs_code_model['کد مدل']
# Process each query
for i, qu in enumerate(query):
    print(f"Processing query {i+1}: {qu}")
    driver.get("https://www.google.com")
    
    # Search for the product model
    search_box = waits.until(EC.element_to_be_clickable((By.NAME, 'q')))
    search_box.send_keys(qu + Keys.ENTER)

    # Wait for search results to load
    try:
        search_results = waits.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.tF2Cxc')))
    except TimeoutException:
        print(f"Timeout while waiting for search results for query: {qu}")
        continue

    found = False
    for result in search_results:
        try:
            link = result.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            if 'digikala.com' in link:
                print(f"Found Digikala link for {qu}: {link}")
                driver.get(link)

                # Click on feature sections
                featurs_1 = waits.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[1]/div[3]/div[3]/div[2]/div[2]/div[2]/div[2]/div[2]/div[1]/div[3]/button')))
                featurs_1.click()
                featurs_2 = waits.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[1]/div[3]/div[3]/div[2]/div[5]/div[2]/div/section/span')))
                featurs_2.click()

                # Scroll down to load all elements
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                headers = waits.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'styles_SpecificationAttribute__value__CQ4Rz')))
                values = waits.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.styles_SpecificationAttribute__valuesBox__gvZeQ div.grow p.break-words:first-of-type')))

                # Set common headers from the first query only
                if i == 0 and common_headers is None:
                    common_headers = set()
                    for index, head in enumerate(headers):
                        common_headers.add(head.text)
                        header_index_map[head.text] = index  # Map header to its original index
                    print(f"Common headers set from first query: {common_headers}")

                # Create a dictionary for the model with values aligned to common headers
                model_dict = {'id': model_id, 'model_code': qu}
                header_list = [head.text for head in headers]  # Current query's headers
                value_list = [val.text for val in values]     # Current query's values

                # Map values to common headers based on their original indices
                for common_head in common_headers:
                    if common_head in header_list:
                        current_index = header_list.index(common_head)  # Find header in current query
                        original_index = header_index_map[common_head]  # Get its original index
                        if current_index < len(value_list):
                            model_dict[common_head] = value_list[current_index]
                        else:
                            model_dict[common_head] = None  # No corresponding value
                    else:
                        model_dict[common_head] = None  # Header not found in this query

                models_data.append(model_dict)
                model_id += 1
                found = True
                break  # Exit loop after finding the first Digikala link

        except StaleElementReferenceException:
            print("Stale element reference encountered, retrying...")
            continue
        except Exception as e:
            print(f"Error processing search result: {e}")
            continue

    if not found:
        print(f"No Digikala link found for {qu}")

# Convert to DataFrame and save to CSV
models_df = pd.DataFrame(models_data)
models_df.to_csv('models_data.csv', index=False, encoding='utf-8-sig')
print("Data saved to models_data.csv")
input('Press any key to exit...')