from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from pathlib import Path
import shutil
from datetime import datetime, timedelta
import time
import json
import logging
from dotenv import load_dotenv



####################
# Setup variables  #
####################

# Load environment variables from .env file
load_dotenv()

# Retrieve variables from environment
email = os.getenv("EMAIL")

# Setup logging
logging.basicConfig(
    filename='yahoo_finance_scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Setup WebDriver
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

# Folder were files will be downloaded IN
downloads_path = os.path.expanduser("~/Downloads")  # MAC/Linux users
# For Windows: downloads_path = "C:\\Users\\<your-username>\\Downloads"
# Folders were files will be moved OUT ( Change as need it)

# Navigate to the ticker's key statistics page
# tickers = ["AAPL", "TSLA", "NFLX", "META", "NVDA", "MSFT", "AMZN", "GOOG"]
# tickers = ["AAPL",] # testing scrapping
with open("company_tickers.json", "r") as file:
    data = json.load(file)
# create the list of tickers which will be processed to get the history
tickers = [data[i]['ticker'] for i in data.keys()]

# Yahoo statements
statements = ["financials", "balance-sheet", "cash-flow"]

# Destination folder for download files
dest_folder = Path(os.getenv("DEST_FOLDER"))

# Open Yahoo Finance and login
logging.info("Opening Yahoo Finance login page")
driver.get("https://login.yahoo.com/")
email_input = wait.until(EC.element_to_be_clickable((By.NAME, "username")))
email_input.send_keys(email)
email_input.send_keys(Keys.RETURN)

# Wait for 2FA completion
logging.info("Waiting for 2FA authentication")
WebDriverWait(driver, 25).until(EC.url_matches(r"^https://www\.yahoo\.com/.*"))


####################
# Helper Functions #
####################
def get_latest_file(directory):
    """Returns the most recently downloaded files from a directory."""
    files = [os.path.join(directory, f) for f in os.listdir(directory)]
    return max(files, key=os.path.getctime) if files else None

# Define function to move the files to a designated folder / tick
def move_file_to_folder(file_path, ticker):
    """Moves the downloaded files to another folder/ticker."""
    try:
        destination_folder = dest_folder / ticker
        # Create the folder if it doesn't exist
        destination_folder.mkdir(parents=True, exist_ok=True)

        # Move files to the designated folder
        new_location = destination_folder / os.path.basename(file_path)
        shutil.move(file_path, new_location)
        logging.info(f"Moved {os.path.basename(file_path)} to {new_location}")
    except Exception as e:
        logging.error(f"Error moving file for ticker {ticker}: {e}")


def download_data(ticker):
    """ Define function to download data for any visible tab"""
    try:
        logging.info(f"Attempting to download data for {ticker}")
        time.sleep(3)  # Allow page to be loaded as download button is already there
        # Wait for the download button and click it
        download_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='download-link']")))
        download_button.click()
        logging.info("Download initiated")
        time.sleep(2)  # Allow download to complete

        latest_file = get_latest_file(downloads_path)
        if latest_file and not latest_file.endswith(".crdownload"):
            move_file_to_folder(latest_file, ticker)
    except Exception as e:
        logging.error(f"Error downloading data for {ticker}: {e}")


#  Define a function to switch tabs and download data
def switch_and_download(period, T):
    try:
        # Switching to period
        wait.until(EC.presence_of_element_located((By.ID, f"tab-{period.lower()}")))
        time.sleep(2)  # Allow page to be loaded as download is already there
        # Switch to the required tab
        period_button = wait.until(EC.element_to_be_clickable((By.ID, f"tab-{period.lower()}")))
        period_button.click()
        logging.info(f"Switched to {period} tab for {ticker}")
        # Ensure the tab content loads before downloading
        time.sleep(2)
        # Download data after switching tabs
        download_data(T)
    except Exception as e:
        logging.error(f"Error switching to {period} tab for {ticker}: {e}")


def generate_date_range():
    """Generate the current date range string (e.g., 'Oct 26, 2023 - Oct 26, 2024')."""
    today = datetime.today()
    previous_yearDate = f"{datetime.today().strftime('%b')} {today.day}, {today.year -1}"
    start_date = today.strftime("%b %d, %Y")
    logging.info(f"Generating date range {previous_yearDate} - {start_date}")
    return f"{previous_yearDate} - {start_date}"


def select_max_date_range():
    """Select the 'Max' date range option."""
    try:
        date_range = generate_date_range()
        logging.info(f"Looking for date range: {date_range}")
        # Find the button with the dynamically generated date range
        date_button = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[@title='{date_range}']")))
        date_button.click()
        max_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@value='MAX']")))
        max_option.click()
        logging.info("Selected 'Max' date range")
        time.sleep(1)
    except Exception as e:
        logging.error(f"Error selecting Max date range: {e}")


def switch_tab(tab_name):
    """Switch between Annual and Quarterly tabs."""
    try:
        tab_button = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[@id='tab-{tab_name.lower()}']")))
        tab_button.click()
        logging.info(f"Switched to {tab_name} tab")
        time.sleep(3)
    except Exception as e:
        logging.error(f"Error switching to {tab_name} tab: {e}")


def navigate_to_statement(ticker, statement):
    """Navigate to the Income Statement, Balance Sheet, or Cash Flow page."""
    try:
        driver.get(f"https://finance.yahoo.com/quote/{ticker}/{statement}/")
        print(f"Navigated to {statement} for {ticker}.")
        time.sleep(3)  # Wait for page to load
    except Exception as e:
        print(f"Error navigating to {statement} for {ticker}: {e}")

def wait_for_table_data():
    """Wait for the historical data table to load with at least one row."""
    try:
        logging.info("Waiting for historical data table to load")
        # 2nd row (first is usually the header)
        table_row = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//table//tr[2]")))
        logging.info("Table data loaded successfully")
    except Exception as e:
        logging.error(f"Error waiting for table data: {e}")

##########
# Step 2:#
##########

for ticker in tickers:
    try:
        # 1. Download Key Statistics
        driver.get(f"https://finance.yahoo.com/quote/{ticker}/key-statistics/")
        logging.info(f"Downloading Quarterly data for {ticker} (default view)...")
        # Get default page (quarterly).
        download_data(ticker)

        # Switch to Annual and Monthly tabs and download data
        for period in ["Annual", "Monthly"]:
            logging.info(f"Downloading {period} data for {ticker}...")
            switch_and_download(period, ticker )
            time.sleep(2)  # Give time for each download to complete

        # 2. Download Key history
        driver.get(f"https://finance.yahoo.com/quote/{ticker}/history/")
        time.sleep(3)  # Allow page to be fully loaded, safer
        logging.info(f"Downloading history OHLCV data for {ticker}...")
        select_max_date_range()
        wait_for_table_data()
        download_data(ticker)

        # 3. Download financials - Income Statement
        driver.get(f"https://finance.yahoo.com/quote/{ticker}/financials/")
        logging.info(f"Downloading Quarterly and Annually financials data for {ticker}...")
        download_data(ticker)
        switch_tab("Quarterly")
        download_data(ticker)

        # 4. Download financials - Balance Sheet
        driver.get(f"https://finance.yahoo.com/quote/{ticker}/balance-sheet/")
        logging.info(f"Downloading Quarterly and Annually balance-sheet data for {ticker}...")
        download_data(ticker)
        switch_tab("Quarterly")
        download_data(ticker)

        # 4. Download financials - Balance Sheet
        driver.get(f"https://finance.yahoo.com/quote/{ticker}/cash-flow/")
        logging.info(f"Downloading Quarterly and Annually cash-flow data for {ticker}...")
        download_data(ticker)
        switch_tab("Quarterly")
        download_data(ticker)
    except Exception as e:
        logging.error(f"Error processing {ticker}: {e}")

# Close the browser
driver.quit()