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
Tickers = all_stocks_list.index.to_list()
# get cummulative weighted index
CWI_history = ftse.Get_CWI_History(start_date='1392-01-01', end_date='1402-01-01',
                          ignore_date=False, just_adj_close=False,
                          show_weekday=True, double_date=True)
# change index date to Christian calender
CWI_history.index = CWI_history['Date']

mpl.plot(CWI_history[-350:], type='candle', mav=(15, 50))
plot.show()

mpl.plot(CWI_history[-420:], type='ohlc', mav=(25, 100))
plot.show()

CWI_history = ftse.Get_CWI_History(start_date='1392-01-01', end_date='1402-01-01',
                          ignore_date=False, just_adj_close=False,
                          show_weekday=True,  double_date=True)

EWI_History = ftse.Get_EWI_History(start_date='1392-01-01', end_date='1402-01-01',
                          ignore_date=False, just_adj_close=False,
                          show_weekday=True, double_date=True)

CWI = CWI_history['Adj Close'].to_numpy()
EWI = EWI_History['Adj Close'].to_numpy()

plot.subplot(1, 2, 1)
plot.plot(CWI, ls='-', lw=1, c='crimson')
plot.title('Tehran Stock Exchange CWI')
plot.xlabel('Time')
plot.ylabel('Value')
plot.yscale('log')

plot.subplot(1, 2, 2)
plot.plot(EWI, ls='-', lw=1, c='crimson')
plot.title('Tehran Stock Exchange EWI')
plot.xlabel('Time')
plot.ylabel('Value')
plot.yscale('log')

plot.show()

PCC = 100 * stat.pearsonr(CWI, EWI)[0]

plot.scatter(CWI, EWI, s=10, color='crimson')
plot.title(f'Tehran Stock Exchange CWI & EWI Correlation (PCC: {round(PCC, 2)} %)')
plot.xlabel('CWI')
plot.ylabel('EWI')
plot.show()

CWI_logplot = np.log(CWI)
EWI_logplot = np.log(EWI)

PCC = 100 * stat.pearsonr(CWI_logplot, EWI_logplot)[0]

plot.scatter(CWI_logplot, EWI_logplot, s=10, color='crimson')
plot.title(f'Tehran Stock Exchange log(CWI) & log(EWI) Correlation (PCC: {round(PCC, 2)} %)')
plot.xlabel('log(CWI)')
plot.ylabel('log(EWI)')
plot.show()

delta_CWI_logplot = CWI_logplot[1:] - CWI_logplot[:-1]
delta_EWI_logplot = EWI_logplot[1:] - EWI_logplot[:-1]

PCC = 100 * stat.pearsonr(delta_CWI_logplot, delta_EWI_logplot)[0]

plot.scatter(delta_CWI_logplot, delta_EWI_logplot, s=10, color='crimson')
plot.title(f'Tehran Stock Exchange delta_(log(CWI)) & delta_(log(EWI)) Correlation (PCC: {round(PCC, 2)} %)')
plot.xlabel('delta_(log(CWI))')
plot.ylabel('delta_(log(EWI))')
plot.show()

price_history = ftse.Get_Price_History(stock='شصدف',
                            start_date='1395-01-01', end_date='1402-01-01',
                            ignore_date=False, adjust_price=True,
                            show_weekday=True, double_date=True)

headers = ['Open', 'High', 'Low', 'Close', 'Final',
            'No', 'Ticker', 'Name', 'Part']

price_history.drop(columns=headers, axis=1, inplace=True)

RenameDict = {'Adj Open': 'Open',
              'Adj High': 'High',
              'Adj Low': 'Low',
              'Adj Close': 'Close',
              'Adj Final': 'Final'}

price_history.rename(columns=RenameDict, inplace=True)

market_watch = ftse.Get_MarketWatch(save_excel=False)
