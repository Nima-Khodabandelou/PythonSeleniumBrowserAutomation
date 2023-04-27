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

DF1 = ftse.Build_Market_StockList(detailed_list=False, payeh=True, bourse=True,
                                 farabourse=True, show_progress=True,
                                 save_excel=False, save_csv=False)

print(DF1.head())

Tickers = DF1.index.to_list()

DF2 = ftse.Get_CWI_History(start_date='1392-01-01',
                          end_date='1402-01-01',
                          ignore_date=False,
                          just_adj_close=False,
                          show_weekday=True,
                          double_date=True)

DF2.index = DF2['Date']

mpl.plot(DF2[-200:], type='candle', mav=(15, 50))
plot.show()

mpl.plot(DF2[-200:], type='ohlc', mav=(15, 70))
plot.show()

DF2 = ftse.Get_CWI_History(start_date='1392-01-01', end_date='1402-01-01',
                          ignore_date=False, just_adj_close=False,
                          show_weekday=True,  double_date=True)

DF3 = ftse.Get_EWI_History(start_date='1392-01-01', end_date='1402-01-01',
                          ignore_date=False, just_adj_close=False,
                          show_weekday=True, double_date=True)

CWI = DF2['Adj Close'].to_numpy()
EWI = DF3['Adj Close'].to_numpy()

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

logCWI = np.log(CWI)
logEWI = np.log(EWI)

PCC = 100 * stat.pearsonr(logCWI, logEWI)[0]

plot.scatter(logCWI, logEWI, s=10, color='crimson')
plot.title(f'Tehran Stock Exchange log(CWI) & log(EWI) Correlation (PCC: {round(PCC, 2)} %)')
plot.xlabel('log(CWI)')
plot.ylabel('log(EWI)')
plot.show()

difflogCWI = logCWI[1:] - logCWI[:-1]
difflogEWI = logEWI[1:] - logEWI[:-1]

PCC = 100 * stat.pearsonr(difflogCWI, difflogEWI)[0]

plot.scatter(difflogCWI, difflogEWI, s=10, color='crimson')
plot.title(f'Tehran Stock Exchange diff(log(CWI)) & diff(log(EWI)) Correlation (PCC: {round(PCC, 2)} %)')
plot.xlabel('diff(log(CWI))')
plot.ylabel('diff(log(EWI))')
plot.show()

DF4 = ftse.Get_Price_History(stock='شصدف',
                            start_date='1395-01-01', end_date='1402-01-01',
                            ignore_date=False, adjust_price=True,
                            show_weekday=True, double_date=True)

DropList = ['Open', 'High', 'Low', 'Close', 'Final',
            'No', 'Ticker', 'Name', 'Part']

DF4.drop(columns=DropList, axis=1, inplace=True)

RenameDict = {'Adj Open': 'Open',
              'Adj High': 'High',
              'Adj Low': 'Low',
              'Adj Close': 'Close',
              'Adj Final': 'Final'}

DF4.rename(columns=RenameDict, inplace=True)

DF5 = ftse.Get_MarketWatch(save_excel=False)
