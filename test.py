import design_portfolio.data as dt
import pandas as pd
names=['BSR', 'LHG', 'SGP', 'VPB', 'CTG']
start_date = '2019-11-15'
end_date = '2022-11-15'
loader=dt.DataLoad(symbols=names, start=start_date, end=end_date)
properties=str(loader.properties(vizual=False))
print(properties)
