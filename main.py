from selenium import webdriver
import os
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get(os.getenv('WORKDAY_URL'))
time.sleep(5)

username_input = driver.find_element(By.ID, 'input28')
username_input.send_keys(os.getenv('WORKDAY_USERNAME'))

# Enter password
password_input = driver.find_element(By.ID, 'input36')
password_input.send_keys(os.getenv('WORKDAY_PASSWORD'))

# Click the "Sign In" button
sign_in_button = driver.find_element(By.CLASS_NAME, 'o-form-button-bar')
sign_in_button.click()

# Wait for Okta 2FA page to load
time.sleep(15)

wait = WebDriverWait(driver, 20)
menu_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(@class, "wdappchrome-af") and text()="MENU"]')))
menu_button.click()

wait = WebDriverWait(driver, 20)
time_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-automation-id='globalNavAppItemLabel' and contains(@class, 'css-49wvux-ItemLabel')]/span[@data-automation-id='truncatedText']/span/span[contains(text(), 'Time')]")))
time_option.click()

this_week_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@title, 'This Week')]")))
this_week_button.click()

# Get today's date
today = datetime.now()

# Determine the month prefix for the dayCell
month_prefix_mapping = {
    1: 0,  # January
    2: 1,  # February
    3: 2,  # March
    4: 3,  # April
    5: 4,  # May
    6: 5,  # June
    7: 6,  # July (based on your observations)
    8: 7,  # August
    9: 8,  # September
    10: 9,  # October
    11: 10,  # November
    12: 11   # December
}

# Get the prefix for the current month
month_prefix = month_prefix_mapping[today.month]

# Calculate the dayCell ID
day_cell_id = f"dayCell-{month_prefix}-{today.day}"

print(f"Day Cell ID: {day_cell_id}")

# Find the cell for today's date
day_cell_xpath = f"//div[@data-automation-id='{day_cell_id}']"
day_cell = wait.until(EC.presence_of_element_located((By.XPATH, day_cell_xpath)))

# Move to the element and click 90 pixels below it
actions = ActionChains(driver)
actions.move_to_element_with_offset(day_cell, 0, 90).click().perform()

# Wait for the "In" field and enter the time
in_field = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-metadata-id='56$187009']//input[@type='text']")))
in_field.send_keys(os.getenv('IN_TIME'))

# Wait for the "Out" field and enter the time
out_field = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-metadata-id='56$187008']//input[@type='text']")))
out_field.send_keys(os.getenv('OUT_TIME'))

ok_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='OK']")))
ok_button.click()
