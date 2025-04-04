from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re
import pandas as pd
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException


options = Options()
options.headless = True  # Run Chrome without a UI
options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass bot detection
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")

driver = webdriver.Chrome(options=options)
waits = WebDriverWait(driver,10)
driver.get("https://torob.com/p/91f20bbc-3564-4dd8-bdcf-7166fc68e285/%DB%8C%D8%AE%DA%86%D8%A7%D9%84-%D8%B3%D8%A7%DB%8C%D8%AF-%D8%A8%D8%A7%DB%8C-%D8%B3%D8%A7%DB%8C%D8%AF-%D8%AF%D9%88%D9%88-34-%D9%81%D9%88%D8%AA-%D9%85%D8%AF%D9%84-sxi30-20s/")
try:
    price_no_discount = waits.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="cheapest-seller"]/div[1]/div[2]'))).text
except TimeoutException:
    # Handle the case where the element isn't found
    price_no_discount = None  # or any default value you prefer
    print("Element not found, continuing execution...")
headers_torob = waits.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.jsx-d9bfdb7eefd5a6bf div.detail-title')))
values_torob = waits.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.jsx-d9bfdb7eefd5a6bf div.detail-value')))
ths = []
vls = []
models_data = []
model_id = 1  # Start with an ID for the first model

# Example loop over multiple models (You will need to implement the logic to get model data)
# Assuming you have a list of model codes to iterate through
model_codes = ['X1', 'X2']  # Replace with your actual model codes
model_dict = {'id': model_id, 'model_code': 'SXi15-21W','price':price_no_discount}  # Create a dictionary for the model

for i, head in enumerate(headers_torob):
    th = head.text  # Header
    v = values_torob[i].text  # Corresponding value
    model_dict[th] = v  # Add header-value pair to the model dictionary
    print(th, v)
models_data.append(model_dict)  # Append the model dictionary to the list
model_id += 1  # Increment the model ID for the next iteration
print(models_data)



input('press any key')