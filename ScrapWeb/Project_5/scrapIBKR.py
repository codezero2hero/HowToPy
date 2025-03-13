import time
import polars as pl
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# Set up Selenium WebDriver
chrome_options = Options()
# chrome_options.add_argument("--headless") # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(options=chrome_options)

# Open the IBKR webpage
url = "https://www.interactivebrokers.com/en/trading/products-exchanges.php#/#"
driver.get(url)

# Give it some time to load
wait = WebDriverWait(driver, 10)

# Accept in headless the first pop-up to move further with the process
try:
    # Wait for the cookie popup and accept/reject it
    cookie_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept Cookies')]"))
    )
    cookie_button.click()
    print("Accepted Cookies")
except:
    print("No cookie popup detected, continuing...")

# Accept in headless the first pop-up to move further with the process
try:
    # Wait for the popup and click "Stay on US website"
    stay_us_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Stay on US website')]"))
    )
    stay_us_button.click()
    print("Stayed on US website")
except:
    print("No location popup detected, continuing...")


# STEP 1: Expand the "Products" dropdown
try:
    products_dropdown = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@id='acc-products']/div[contains(@class, 'accordion_btn')]")))
    products_dropdown.click()
    time.sleep(1)  # Wait for dropdown to expand
except:
    print("Products dropdown already expanded")

# Select "Stocks" checkbox
stocks_checkbox = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//span[contains(text(), 'Stocks')]/preceding-sibling::input")))
stocks_checkbox.click()

# Click "Apply" button
apply_button = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//button[contains(text(), 'Apply')]")))
apply_button.click()

# Wait for table to load
wait = WebDriverWait(driver, 2)

# Step 2: Expand the "Regions" dropdown and select "United States"
region = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//span[contains(text(), 'Regions')]")))
region.click()

us_checkbox = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//span[contains(text(), 'United States')]/preceding-sibling::input")))
us_checkbox.click()

# Click "Apply" button
apply_button = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//button[contains(text(), 'Apply')]")))
apply_button.click()

# Wait for table to load
wait = WebDriverWait(driver, 2)

# Step 2: Select "Show 500 Rows Per Page"
time.sleep(5)  # Wait for filters to apply
rows_per_page = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@aria-label='Choose rows per page']")))
select = Select(rows_per_page)
select.select_by_value("500")  # Selects the option to show 500 rows
time.sleep(5)  # Wait for data reload

# Step 3: Extract Table Data with Pagination
all_data = []

# Extract the total number of pages
total_pages_element = driver.find_element(By.CSS_SELECTOR, ".form-pagination span")
total_pages = int(total_pages_element.text)

current_page = 1

while current_page <= total_pages:
    # Locate table
    table = wait.until(EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'table')]")))

    # Extract headers if not set
    if not all_data:
        headers = [th.text.strip() for th in table.find_elements(By.TAG_NAME, "th")]

    # Extract rows
    rows = []
    for row in table.find_elements(By.TAG_NAME, "tr")[1:]:  # Skip header row
        columns = row.find_elements(By.TAG_NAME, "td")
        rows.append([col.text.strip() for col in columns])

    all_data.extend(rows)

    # Check if next button exists and we haven't exceeded the last page
    next_button = driver.find_element(By.CLASS_NAME, "btn-forward")
    print(f"{current_page} out of {total_pages}...Done!")

    if current_page == total_pages:
        break  # Stop if we are at the last page

    next_button.click()
    time.sleep(3)  # Wait for next page to load
    current_page += 1  # Increment page count

# Step 4: Convert Data to Polars DataFrame, clean and Save
# orient=row ensures Polars correctly interprets all_data as rows, not columns.
df = pl.DataFrame(all_data, schema=headers, orient="row")

# Remove the * from words which indicate primary exchange, we dont need.
df = df.with_columns(df['EXCHANGE  *PRIMARY EXCHANGE'].str.replace("*", "", literal=True))

# Remove symbols which are not matching between SYMBOL and IBKR SYMBOL
df = df.filter(df["SYMBOL"] == df["IBKR SYMBOL"])

# Remove unused columns
df = df.drop(['CURRENCY', 'PRODUCT', 'REGION', 'IBKR SYMBOL'])

# Rename remaining columns to be more user-friendly
df = df.rename({"EXCHANGE  *PRIMARY EXCHANGE": "IBKR_EXCHANGE"})

# Step 5: Save data in csv format
# Output everything into a clean CSV
df.write_csv("interactive_brokers_us_stocks.csv")

# Display DataFrame
print(df)

# Close the browser
driver.quit()