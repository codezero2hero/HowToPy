from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd

# Initialized the webdrive (Chrome, Firefox etc can be used)
driver = webdriver.Chrome()

# Page which will be scrapped
url = "https://stockanalysis.com/list/nasdaq-stocks/"

# This is connected with how many subpages currently the page has to present all NASDAQ symbols
pages = 7

# List to store all table rows, one by one
all_rows = []

# Navigate to the URL
driver.get(url)

for i in range(1, pages + 1):
    # Wait for the page and elements to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "tbody"))
    )

    # Pull the content of the page into a variable
    html_content = driver.page_source

    # Read the html contect with beautifulsoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract data, skipping the first 'td' using slicing inside the loop
    tbody = soup.find('tbody')
    for tr in tbody.find_all('tr'):
        row = [td.text for td in tr.find_all('td')[1:]]  # Skipping the first td here
        all_rows.append(row)

    # Handle 'Next' button click if not last page
    if i < pages:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Next')]"))
        )
        next_button.click()
        time.sleep(1)  # Wait a moment for the page to load

# Close the driver
driver.quit()

# Create DataFrame after collecting all rows
stocks = pd.DataFrame(all_rows, columns=["Symbol", "CompanyName", "MarketCap", "StockPrice", "%Change", "Revenue"])

# print(stocks)

# Output the dataframe into a CSV without index
#stocks.to_csv("nasdaqStocks.csv", index=False)

# Let's have some fun with the output
# I want to have a list of stocks which has the revenue in B and organize them in an ascending order
stocks['BMK'] = stocks['Revenue'].str.extract(r'([BMK])$')

# Let's change the NaN values which come from - in the Revenue with N/A
stocks['BMK'] = stocks['BMK'].fillna('N/A')

# Function to strip 'B', 'M', or 'K' from each string in the Revenue column
def remove_bmk_suffix(value):
    if value == '-':
        return '0'  # Replace placeholder '-' with '0'
    return value.rstrip('BMK')  # Strip 'B', 'M', or 'K' from the right


# Apply the function to remove the suffixes from the 'Revenue' column
stocks['Revenue'] = stocks['Revenue'].apply(remove_bmk_suffix)

# Optionally, convert the 'Revenue' column to a numeric type
stocks['Revenue'] = pd.to_numeric(stocks['Revenue'], errors='coerce')

# Filter rows where 'BMK' is 'B' and revenue is greater than 100
billions_df = stocks[(stocks['BMK'] == 'B') & (stocks['Revenue'] > 10)]

# Sort rows by 'Revenue' in descending order
sorted_billions_df = billions_df.sort_values(by='Revenue', ascending=False)

# Capture the result in a dataframe for further use
result = sorted_billions_df[['Symbol', 'CompanyName', 'Revenue']]
