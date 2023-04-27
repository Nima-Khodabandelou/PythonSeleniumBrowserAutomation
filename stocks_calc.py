# numpy and pandas are used for calculation instead of simple list operastions.
import numpy as np
import pandas as pd
# finpy_ftse is a python package developed to access Tehran stock market data
import finpy_ftse as ftse
# for financial plotting purpose
import mplfinance as mpl
# calculate statistical functions
import scipy.stats as stat
# for general plot
import matplotlib.pyplot as plot


# set style for plot
plot.style.use('ggplot')

# get all stocks list in each market, i.e. bourse, payeh, and farabourse
all_stocks_list = ftse.Build_Market_StockList(detailed_list=False, payeh=True, bourse=True,
                                 farabourse=True, show_progress=True,
                                 save_excel=False, save_csv=False)

# print the first 5 items
print(all_stocks_list.head())
# print all items
all_tickers = all_stocks_list.index.to_list()
# get cummulative weighted index
cummulative_weighted_index_history = ftse.Get_cummulative_weighted_index_History(start_date='1392-01-01', end_date='1402-01-01',
                          ignore_date=False, just_adj_close=False,
                          show_weekday=True, double_date=True)
# change index date to Christian calender
cummulative_weighted_index_history.index = cummulative_weighted_index_history['Date']

mpl.plot(cummulative_weighted_index_history[-350:], type='candle', mav=(15, 50))
plot.show()

mpl.plot(cummulative_weighted_index_history[-420:], type='ohlc', mav=(25, 100))
plot.show()

cummulative_weighted_index_history = ftse.Get_cummulative_weighted_index_History(start_date='1392-01-01', end_date='1402-01-01',
                          ignore_date=False, just_adj_close=False,
                          show_weekday=True,  double_date=True)

equal_weighted_index_History = ftse.Get_equal_weighted_index_History(start_date='1392-01-01', end_date='1402-01-01',
                          ignore_date=False, just_adj_close=False,
                          show_weekday=True, double_date=True)

cummulative_weighted_index = cummulative_weighted_index_history['Adj Close'].to_numpy()
equal_weighted_index = equal_weighted_index_History['Adj Close'].to_numpy()

plot.subplot(1, 2, 1)
plot.plot(cummulative_weighted_index, ls='-', lw=1, c='blue')
plot.title('cummulative_weighted_index')
plot.xlabel('Time')
plot.ylabel('price')
plot.yscale('logarithmic')

plot.subplot(1, 2, 2)
plot.plot(equal_weighted_index, ls='-', lw=1, c='blue')
plot.title('equal_weighted_index')
plot.xlabel('Time')
plot.ylabel('price')
plot.yscale('logarithmic')

plot.show()

PCC = 100 * stat.pearsonr(cummulative_weighted_index, equal_weighted_index)[0]

plot.scatter(cummulative_weighted_index, equal_weighted_index, s=10, color='blue')
plot.title(f'cummulative_weighted_index and equal_weighted_index correl. (PCC: {round(PCC, 2)} %)')
plot.xlabel('cummulative_weighted_index')
plot.ylabel('equal_weighted_index')
plot.show()

cummulative_weighted_index_logplot = np.log(cummulative_weighted_index)
equal_weighted_index_logplot = np.log(equal_weighted_index)

PCC = 100 * stat.pearsonr(cummulative_weighted_index_logplot, equal_weighted_index_logplot)[0]

plot.scatter(cummulative_weighted_index_logplot, equal_weighted_index_logplot, s=10, color='blue')
plot.title(f'log(cummulative_weighted_index) & log(equal_weighted_index) correl. (PCC: {round(PCC, 2)} %)')
plot.xlabel('log(cummulative_weighted_index)')
plot.ylabel('log(equal_weighted_index)')
plot.show()

delta_cummulative_weighted_index_logplot = cummulative_weighted_index_logplot[1:] - cummulative_weighted_index_logplot[:-1]
delta_equal_weighted_index_logplot = equal_weighted_index_logplot[1:] - equal_weighted_index_logplot[:-1]

PCC = 100 * stat.pearsonr(delta_cummulative_weighted_index_logplot, delta_equal_weighted_index_logplot)[0]

plot.scatter(delta_cummulative_weighted_index_logplot, delta_equal_weighted_index_logplot, s=10, color='blue')
plot.title(f'delta_(log(cummulative_weighted_index)) & delta_(log(equal_weighted_index)) correl. (PCC: {round(PCC, 2)} %)')
plot.xlabel('delta_(log(cummulative_weighted_index))')
plot.ylabel('delta_(log(equal_weighted_index))')
plot.show()

stock_name = 'شصدف'
price_history = ftse.Get_Price_History(stock=stock_name, start_date='1395-01-01', end_date='1402-01-01',
                            ignore_date=False, adjust_price=True, show_weekday=True, double_date=True)

headers = ['Open', 'High', 'Low', 'Close', 'Final', 'No', 'Ticker', 'Name', 'Part']

price_history.drop(columns=headers, axis=1, inplace=True)

RenameDict = {'Adj Open': 'Open', 'Adj High': 'High',
              'Adj Low': 'Low', 'Adj Close': 'Close',
              'Adj Final': 'Final'}

price_history.rename(columns=RenameDict, inplace=True)

market_watch = ftse.Get_MarketWatch(save_excel=False)
