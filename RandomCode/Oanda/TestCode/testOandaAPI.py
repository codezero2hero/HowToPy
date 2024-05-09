# Test OandaAPI connectivity and print the output
"""
import requests
from dotenv import load_dotenv
import os

# load variables from file
load_dotenv()

account_id = os.getenv('OANDA_ACCOUNT_ID')
access_token = os.getenv('OANDA_ACCESS_TOKEN')

# API URL for retrieving data (example:getaccounts)
url = f"https://api-fxpractice.oanda.com/v3/accounts"

# Setup headers to include your access token for authentication
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {access_token}'
}

# Make GET request to API
response = requests.get(url, headers=headers)

# Print the status code and data
print("StatusCode:", response.status_code)
print("JSONResponse:", response.json())
"""


# Get OandaAPI account details and print the output
"""
import requests
from dotenv import load_dotenv
import os

# load variables from file
load_dotenv()

account_id = os.getenv('OANDA_ACCOUNT_ID')
access_token = os.getenv('OANDA_ACCESS_TOKEN')

# API URL for retrieving data (example:getaccounts)
url = f"https://api-fxpractice.oanda.com/v3/accounts"

# Setup headers to include your access token for authentication
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {access_token}'
}

# Make GET request to API
response = requests.get(url, headers=headers)

# Print the status code and data
print("StatusCode:", response.status_code)
print("JSONResponse:", response.json())
"""


# Get all instruments to which your account has access
"""
import requests
from dotenv import load_dotenv
import os

# Load variables from file
load_dotenv()

account_id=os.getenv('OANDA_ACCOUNT_ID')
access_token=os.getenv('OANDA_ACCESS_TOKEN')


# API URL for retrieving data (example:getaccounts)
url=f"https://api-fxpractice.oanda.com/v3/accounts/{account_id}/instruments"

# Setup headers to include your access token for authentication
headers={
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {access_token}'
}

# Makea GET request to API
response = requests.get(url,headers=headers)

# Print the status code and data
print("StatusCode:", response.status_code)
print("JSONResponse:", response.json())

# Creating the list of instruments and filling it with content from Oanda
instrs = []
for i in range(len(response.json()['instruments'])):
    instrs.append(response.json()['instruments'][i]['name'])

# Vizualize the instr variable
print(instrs)
"""

# Optimize and make the above code more pythonic
"""
import requests
from dotenv import load_dotenv
import os

# Load variables from file
load_dotenv()

account_id=os.getenv('OANDA_ACCOUNT_ID')
access_token=os.getenv('OANDA_ACCESS_TOKEN')


# API URL for retrieving data (example:getaccounts)
url=f"https://api-fxpractice.oanda.com/v3/accounts/{account_id}/instruments"

# Setup headers to include your access token for authentication
headers={
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {access_token}'
}

# Makea GET request to API
response = requests.get(url,headers=headers)

# Print the status code and data
print("StatusCode:", response.status_code)
print("JSONResponse:", response.json())

# Get the list of instruments that can be traded in Oanda with list comprehension
inst = [response.json()['instruments'][i]['name'] for i in range(len(response.json()['instruments']))]

# OR

# A more pythonic approach is to use the get() function which looks like this
instruments = [inst['name'] for inst in response.json().get('instruments', [])]

# Visualize both variables
print(inst)
print(instruments)
"""

# Get details regarding only one instruments
"""
import requests
from dotenv import load_dotenv
import os

# load variables from file
load_dotenv()

account_id=os.getenv('OANDA_ACCOUNT_ID')
access_token=os.getenv('OANDA_ACCESS_TOKEN')


# API URL for retrieving data (example:getaccounts)
url=f"https://api-fxpractice.oanda.com/v3/accounts/{account_id}/instruments?instruments=EUR_USD"

# Setup headers to include your access token for authentication
headers={
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {access_token}'
}

# Makea GET request to API
response = requests.get(url,headers=headers)

# Print the status code and data
print("StatusCode:", response.status_code)
print("JSONResponse:", response.json())
"""

# Get details regarding a selection of instruments
"""
import requests
from dotenv import load_dotenv
import os

# load variables from file
load_dotenv()

account_id=os.getenv('OANDA_ACCOUNT_ID')
access_token=os.getenv('OANDA_ACCESS_TOKEN')

inst = ['EUR_USD', 'GBP_JPY', 'EUR_JPY']

# API URL for retrieving data (example:getaccounts)
url=f"https://api-fxpractice.oanda.com/v3/accounts/{account_id}/instruments?instruments={','.join(inst)}"

# Setup headers to include your access token for authentication
headers={
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {access_token}'
}

# Makea GET request to API
response = requests.get(url,headers=headers)

# Print the status code and data
print("StatusCode:", response.status_code)
print("JSONResponse:", response.json())
"""

# Wrapping out the code
import requests
from dotenv import load_dotenv
import os

# load variables from file
load_dotenv()

account_id = os.getenv('OANDA_ACCOUNT_ID')
access_token = os.getenv('OANDA_ACCESS_TOKEN')

# API URL for retrieving data (example:getaccounts)
url = f"https://api-fxpractice.oanda.com/v3/accounts/{account_id}/instruments"

# Setup headers to include your access token for authentication
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {access_token}'
}

# Makea GET request to API
response = requests.get(url, headers=headers)

# handling API response
if response.status_code == 200:
    print("Successfully connected to Oanda")

    data = response.json()
    # List comprehencion containing the instruments avoiding a KeyError we add [] in get
    # If the key 'instruments' does not exist, it returns an empty list [] instead.
    instr = [instr['name'] for instr in data.get('instruments', [])]

    print("Instruments available for trading, multiple per line")
    for i in range(0, len(instr), 12):
        # Slice 6 instruments per line to be printed
        six_items = instr[i:i + 12]
        # Print items joined by comma
        print(", ".join(six_items))

else:
    print("Failed to connect to Oanda")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    # maybe you'll need for more context also the json
    print("JSONResponse:", response.json())