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
driver.get("https://www.digikala.com/product/dkp-17291163/%DB%8C%D8%AE%DA%86%D8%A7%D9%84-%D9%88-%D9%81%D8%B1%DB%8C%D8%B2%D8%B1-%D8%B3%D8%A7%DB%8C%D8%AF-%D8%A8%D8%A7%DB%8C-%D8%B3%D8%A7%DB%8C%D8%AF-32-%D9%81%D9%88%D8%AA-%D8%A7%D8%B3%D9%86%D9%88%D8%A7-%D9%85%D8%AF%D9%84-s1di-m210s/")
featurs_1 = waits.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="__next"]/div[1]/div[3]/div[3]/div[2]/div[2]/div[2]/div[2]/div[2]/div[1]/div[3]/button'))).click()
featurs_2 = waits.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="__next"]/div[1]/div[3]/div[3]/div[2]/div[5]/div[2]/div/section/span'))).click()
end_of_scroll = driver.execute_script('return document.body.scrollHeight')
# headers = ['نمودار مصرف انرژی','وزن','گنجایش کل به فوت','گنجایش یخچال','گنجایش فریزر','نوع مقاومت در برابر برفک']
# headers = waits.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#__next > div.h-full.flex.flex-col.bg-neutral-000.items-center > div.grow.bg-neutral-000.flex.flex-col.w-full.items-center.shrink-0 > div.grow.bg-neutral-000.flex.flex-col.w-full.items-center.styles_BaseLayoutDesktop__content__hfHD1.container-4xl-w > div.lg\:px-5 > div:nth-child(5) > div.flex.w-full > div > section > div:nth-child(2) > div > div:nth-child(1) > p')))
headers = driver.find_elements(By.CLASS_NAME,'styles_SpecificationAttribute__value__CQ4Rz')
# values = driver.find_elements(By.CSS_SELECTOR,'div.styles_SpecificationAttribute__valuesBox__gvZeQ div.grow p.break-words')
values = waits.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.styles_SpecificationAttribute__valuesBox__gvZeQ div.grow p.break-words:first-of-type')))
ths = []
vls = []
models_data = []
model_id = 1  # Start with an ID for the first model

# Example loop over multiple models (You will need to implement the logic to get model data)
# Assuming you have a list of model codes to iterate through
model_codes = ['X1', 'X2']  # Replace with your actual model codes
model_dict = {'id': model_id, 'model_code': 'DAEWOO-SBS-DS-3020MW'}  # Create a dictionary for the model

for i, head in enumerate(headers):
    th = head.text  # Header
    v = values[i].text  # Corresponding value
    model_dict[th] = v  # Add header-value pair to the model dictionary
    print(th, v)
# models_data.append(model_dict)  # Append the model dictionary to the list
model_id += 1  # Increment the model ID for the next iteration
print(models_data)



input('press any key')