import nasdaqdatalink as ndl
import pandas as pd

# Add API key for reference to allow access to unrestricted data
#ndl.read_key(filename="../env/.nasdaqdatalinkapikey")
ndl.ApiConfig.api_key = 'xwyvyTy7unp22GRcsqtP'

# Command to pull data
# If start date and end date are not specified the entire data set is included
df = ndl.get_table("WIKI/PRICES", qopts = { 'columns': ['ticker', 'date', 'close'] }, ticker = ['AAPL', 'MSFT'], date = { 'gte': '2022-01-01', 'lte': '2022-12-31' }, paginate=True)

# Sort columns by date ascending
#df.sort_values('date', ascending = True, inplace = True)

# Rename date column
#df.rename(columns = {'date':'Date'}, inplace = True)

# Set index to date column
#df.set_index('Date', inplace = True)

print(f"Data shape: {df.shape}\n", df.head(), df.tail())
