path = "https://www.digikala.com/product/dkp-16474456/%DB%8C%D8%AE%DA%86%D8%A7%D9%84-%D9%88-%D9%81%D8%B1%DB%8C%D8%B2%D8%B1-%D8%B3%D8%A7%DB%8C%D8%AF-%D8%A8%D8%A7%DB%8C-%D8%B3%D8%A7%DB%8C%D8%AF-37-%D9%81%D9%88%D8%AA-%D8%AF%D9%88%D9%88-%D9%85%D8%AF%D9%84-sxi20-31s/"

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re
import pandas as pd
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)


options = Options()
options.headless = True  # Run Chrome without a UI
options.add_argument(
    "--disable-blink-features=AutomationControlled"
)  # Bypass bot detection
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")

driver = webdriver.Chrome(options=options)
waits = WebDriverWait(driver, 10)
driver.get(path)
try:
    price_no_discount = waits.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="__next"]/div[1]/div[3]/div[3]/div[2]/div[2]/div[2]/div[2]/div[4]/div/div[4]/div/div/div/div[1]/div/div[2]/span',
            )
        )
    ).text
except TimeoutException:
    # Handle the case where the element isn't found
    price_no_discount = None  # or any default value you prefer
    print("Element not found, continuing execution...")

ths = []
vls = []
models_data = []
model_id = 1  # Start with an ID for the first model

# Example loop over multiple models (You will need to implement the logic to get model data)
# Assuming you have a list of model codes to iterate through
model_codes = ["X1", "X2"]  # Replace with your actual model codes
model_dict = {
    "id": model_id,
    "model_code": "SXi15-21W",
    "price": price_no_discount,
}  # Create a dictionary for the model

models_data.append(model_dict)  # Append the model dictionary to the list
model_id += 1  # Increment the model ID for the next iteration
print(models_data)


input("press any key")
