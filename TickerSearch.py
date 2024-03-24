import requests
import json

# https://www.alphavantage.co/support/#api-key

user_key = r'insertUserKeyHere'
keywords = 'bae'
url = ('https://www.alphavantage.co/query?function=SYMBOL_SEARCH&'
       'keywords=' + keywords + '&apikey=' + user_key)
r = requests.get(url)
data = r.json()

print(json.dumps(data, indent=4))