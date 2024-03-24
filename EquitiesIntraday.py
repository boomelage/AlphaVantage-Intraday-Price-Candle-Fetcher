###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################

from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import requests
import time 

###############################################################################
###############################################################################
###############################################################################
############################# v1.2 - 18 March 2024 ############################
###############################################################################
###############################################################################
###############################################################################
############################ © BRICIU, Radu Stefan  ###########################
############################## rsbriciu@gmail.com #############################
###############################################################################
###############################################################################
###############################################################################
#
# This script allows its user to retrieve intraday security prices for a given 
# start year (t0), end year (T), frequency (dt), and ticker. There is an output
# section at the end of the code where the user can modify the format or final 
# candle matrix name. It is currently set to export a .csv file with Datetime-
# 64[ns] indexing. The matrix is named 'prices' and containts the following
# columns:
#
#    → datetime
#    → open
#    → low
#    → high
#    → close
#    → volume
#
# The data source used is the AlphaVantage API. You will require a paid key in 
# order to exceed 25 call requests per day. Execution time will depend on sub-
# scription level.
#
###############################################################################
###############################################################################
###############################################################################
################################# USER INPUTS #################################
###############################################################################
###############################################################################
###############################################################################

ticker = "intc"
T = 2024
dt = "1"
# The following integer strings are supported: 
# 1, 5, 15, 30, 60 (minutes)
t0 = 1998
# such that dT > 0
dT = T - t0
user_key = "insertUserKeyHere"

# https://www.alphavantage.co/

###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################

start_time = time.time()

def generate_date_sequence(t0, dT):
    dates = []
    current_date = datetime(t0, 1, 1)
    for _ in range(dT):
        for month in range(1, 13):
            dates.append(current_date.strftime("%Y-%m"))
            current_date += timedelta(days=31)  
            # Adding an approximate month duration
    return dates

def tickers(string, n):
    return [string] * n

def intraDayInterval(string, n):
    return [string] * n

def link1(string, n):
    return [string] * n

def link2(string, n):
    return [string] * n

def link3(string, n):
    return [string] * n

def link4(string, n):
    return [string] * n

dates = generate_date_sequence(t0, dT)
tickers = tickers(ticker, len(dates))
intervals = intraDayInterval(dt, len(dates))
link1s = link1(
    "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="
    , len(dates))
link2s = link2("&interval=", len(dates))
link3s = link3("min&month=", len(dates))
link4s = link4("&outputsize=full&apikey=" + user_key, len(dates))

linkBuilder = np.array([link1s, tickers, link2s, intervals, link3s, dates, 
                        link4s]).T

linkBuilder = pd.DataFrame(linkBuilder)

links = linkBuilder.apply(lambda row: ''.join(row.astype(str)), axis=1)

# List of URLs
urls = links

# List to store DataFrames
dfs = []

# Iterate over each URL
for url in urls:
    try:
        # Request data
        r = requests.get(url)
        data = r.json()
        
        # Check if data contains the required key
        if 'Time Series (' + dt + 'min)' not in data:
            print(f"No data available for {url}")
            continue
        
        # Convert JSON to DataFrame
        df = pd.DataFrame.from_dict(data['Time Series (' + dt + 'min)'], 
                                    orient='index')
        
        # Append DataFrame to list
        dfs.append(df)
    except KeyError as e:
        print(f"KeyError: {e} occurred for {url}")

# Check if any data was retrieved
if not dfs:
    print("No data retrieved. Please check your inputs.")
    # You can choose to exit the script or handle it as appropriate
else:
    prices = pd.concat(dfs)
    prices.index = prices.index.astype('datetime64[ns]')
    prices = prices.rename(columns={'1. open': 'open', '2. high': 'high', 
                                    '3. low': 'low', '4. close': 'close', 
                                    '5. volume': 'volume'})
    prices = prices.astype({col: float for col in prices.columns}).sort_index()
    prices.index.name = 'datetime'
    prices = prices.sort_index()

###############################################################################
#################################### OUTPUT ###################################
###############################################################################

output_file_name = (f"{ticker}_{dt}min_{t0}_{T}.csv")
prices.to_csv(str(output_file_name))
    
###############################################################################
###############################################################################
###############################################################################
############################ © BRICIU, Radu Stefan  ###########################
############################## rsbriciu@gmail.com #############################
###############################################################################
###############################################################################
############################################################################### 

end_time = time.time() 
execution_time = end_time - start_time
print(f"{str(output_file_name)} Exported Successfully ( ͡°👅 ͡°)") 
print(f"Execution time: {execution_time:.1f} seconds")

###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################