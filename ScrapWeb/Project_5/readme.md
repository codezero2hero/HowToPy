# Interactive Brokers Stock Data Scraper

This Python script uses **Selenium** to scrape stock data from the Interactive Brokers website. 
It extracts stock listings based on selected criteria (Products: **Stocks**, Regions: **United States**) and saves the results in a **Polars DataFrame**, which is exported as a CSV file.

## 📌 Features
- **Handles popups** (cookies, location selection)
- **Filters stocks by region (United States)**
- **Selects 500 rows per page** for faster data extraction
- **Handles pagination** to scrape all available pages
- **Extracts stock details into a structured Polars DataFrame**
- **Saves data as a CSV file** for further analysis

---

## 🚀 Installation & Setup

### **1. Install Required Dependencies**
Ensure you have Python installed, then install the required packages in a certain environment:

```bash
pip install selenium polars pandas
```

You also need to install **Google Chrome** and **ChromeDriver**. Ensure they are compatible:
- Download ChromeDriver: [https://sites.google.com/chromium.org/driver/](https://sites.google.com/chromium.org/driver/)
- Place the `chromedriver` executable in your system's PATH or the project folder.
OBS: If you have a MAC, please use brew and work the magic with this.

### **2. Enable API Access in IBKR**
This script does not use IBKR API, but it scrapes IBKR's public web pages. 
Ensure you can manually access [IBKR Trading Products](https://www.interactivebrokers.com/en/trading/products-exchanges.php) in a browser before running the script.

---

## 🛠 How to Run the Script

```bash
python scrapIBKR.py or use an IDE to give it a try.
```

---

## 📝 How It Works

### **1. Launches Chrome and Navigates to IBKR**
- Opens the **IBKR Trading Products** page
- Accepts **Cookies**
- Stays on the **US website**

### **2. Selects Filters**
- Expands **"Products"** dropdown and selects **"Stocks"**
- Clicks **Apply** to update filters
- Expands **"Regions"** dropdown and selects **"United States"**
- Clicks **Apply** to update filters

### **3. Adjusts Rows Per Page**
- Changes to **500 rows per page** for efficient scraping

### **4. Extracts Table Data**
- Retrieves **headers and stock details**
- Iterates through **all pages**
- Stores data in a **Polars DataFrame**
- Removes unnecessary data from the dataframe

### **5. Saves Data as CSV**
- Saves the extracted data as `interactive_brokers_us_stocks.csv`

---

## 📂 Expected Output
The extracted CSV will contain stock details with columns like:

```
SYMBOL, DESCRIPTION, IBKR_EXCHANGE
A, AGILENT TECHNOLOGIES, NYSE
AA, ALCOA CORP, AMEX
AABB, ASIA BROADBAND, OTCLNKECN
```

---

## 🔥 Troubleshooting

### **1. ChromeDriver Version Issues**
If you encounter **"ChromeDriver version mismatch"**, update ChromeDriver:
```bash
chromedriver --version  # Check version
# Download a compatible version from https://chromedriver.chromium.org/downloads
```

### **2. Page Not Loading or XPATH Issues**
- Ensure **IBKR’s page structure has not changed**
- If the script fails at `find_element`, update the **XPATH selectors**
- Increase `time.sleep()` if the page loads slowly

### **3. Handling Popups**
- If new popups appear, inspect them (`F12` in Chrome) and modify `XPATH` selectors in the script.

---

## 👨‍💻 Author
This script was developed to automate stock data retrieval from IBKR and get a full list of stocks.
Contributions and improvements are welcome!

