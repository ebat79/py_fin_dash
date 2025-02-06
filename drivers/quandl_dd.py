import quandl

# Load some data from Quandl
aapl = quandl.get("WIKI/AAPL", authtoken="xwyvyTy7unp22GRcsqtP")
print(aapl.head())
