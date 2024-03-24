import pandas as pd
import time 

file_name = r'2019-03-01_2023-08-31_filter_ubs1min.csv'

start_time = time.time()

# Read the CSV file into a DataFrame
df = pd.read_csv(file_name)

# Convert the timestamp column to datetime format
df['datetime'] = pd.to_datetime(df['datetime'])


# Check for and remove duplicate timestamps
df = df[~df['datetime'].duplicated()]

# Set the timestamp column as the index
df.set_index('datetime', inplace=True)

# Group by day and interpolate within each group
df_interpolated = df.groupby(df.index.date).apply(lambda x: x.resample('1T')
                                                  .interpolate(method=
                                                               'linear'))

# Save the interpolated DataFrame to a new CSV file
df_interpolated.to_csv("interpolated_" + file_name)

end_time = time.time() 
execution_time = end_time - start_time
print("File Exported Successfully ( ͡°👅 ͡°)") 
print(f"Execution time: {execution_time:.1f} seconds")

