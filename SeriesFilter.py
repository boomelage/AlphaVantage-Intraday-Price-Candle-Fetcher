import time 
import pandas as pd

# =============================================================================
# User Inputs
# =============================================================================

filename = "DataArchive/ubs1min_2001_2024.csv"
start_year = '2019-03-01' # can be any datetime64[ns] value
end_year = '2023-08-31'   # can be any datetime64[ns] value
file_identifyer = r'ubs1min'
filtered_series_file_name = (start_year + "_" + end_year + "_" 
                             + "filter" + "_" + file_identifyer +".csv" )

# =============================================================================
# 
# =============================================================================

start_time = time.time()

df = pd.read_csv(filename, index_col = "datetime")
uptrunc = df[df.index >= start_year]
filtered = uptrunc[uptrunc.index <= end_year]

# =============================================================================
# Output
# =============================================================================

filtered.to_csv(filtered_series_file_name)

# =============================================================================
# 
# =============================================================================

end_time = time.time() 
execution_time = end_time - start_time

print("File Exported Successfully ( ͡°👅 ͡°)") 
print(f"Execution time: {execution_time:.1f} seconds")