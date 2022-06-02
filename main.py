import json
import backtrader as bt
import pandas as pd
import quantstats as qs
from numpy import arange
import argparse

__author__ = "Damiano Dotto"
__copyright__ = "Copyright 2022, Quant Trader Academy"
__version__ = "1.0.1"
__email__ = "damiano.dotto95@gmail.com"

from Strategia import Strategia


def generaReport(result):
    returns, positions, transactions, gross_lev = result[0].analyzers.getbyname('pyfolio').get_pf_items()
    returns.index = returns.index.tz_convert(None)
    qs.reports.html(returns, output="output/reportBacktest.html", download_filename="output/reportBacktest.html")


def generaCsv(result):
    optimizationResult = [[json.dumps(x[0].params._getkwargs()),
                           x[0].analyzers.trade.get_analysis()['pnl']['net']['total'],
                           x[0].analyzers.trade.get_analysis()['total']['total'],
                           ] for x in result]

    dfoptimizationResult = pd.DataFrame(optimizationResult, columns=['parametri', 'Profitto Netto', 'totale'])
    dfoptimizationResult = dfoptimizationResult.sort_values(by='Profitto Netto', ascending=False)
    dfoptimizationResult.to_csv('output/reportOptimization.csv', index=False)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--backtest', dest='backtest', action='store_true')
    parser.add_argument('--optimization', dest='backtest', action='store_false')
    parser.set_defaults(action=True)
    args = parser.parse_args()

    # Download data directly from YahooFinance
    # data = bt.feeds.PandasData(dataname=yf.download('GBPJPY=X', '2010-01-01', date.today()))
    data = bt.feeds.YahooFinanceCSVData(dataname='data/GBPJPY.csv')  # Read data from csv
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.broker.setcash(10000.0)  # set initial capital

    # Analyzers
    cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name="drawdown")
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="trade")

    if args.backtest:
        print("Running Backtest...")

        cerebro.addstrategy(Strategia)
        result = cerebro.run()

        generaReport(result)

    else:
        # optimize parameters
        print("Running Optimization...")

        cerebro.optstrategy(Strategia, vincitaMassima=arange(0.2, 3.0, 0.1))
        result = cerebro.run()

        generaCsv(result)
