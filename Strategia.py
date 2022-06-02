import backtrader as bt


class Strategia(bt.Strategy):

    # input parametri strategia
    params = (
        ('perditaMassima', 1.2),
        ('vincitaMassima', 2.0),
    )

    def __init__(self):
        self.prezzoPerditaMassima = None
        self.prezzoVincitaMassima = None
        # load close price, high price and low price
        self.chiusura = self.data.close
        self.massimi = self.data.high
        self.minimi = self.data.low

    def next(self):
        # if not open trades
        if self.getposition().size == 0:
            # buy if close is greater high else sell if close lower than low
            if self.chiusura > self.massimi[-1]:
                self.prezzoPerditaMassima = self.closePrice - self.p.perditaMassima
                self.prezzoVincitaMassima = self.closePrice + self.p.vincitaMassima
                self.buy_bracket(size=60, stopprice=self.prezzoPerditaMassima, limitprice=self.prezzoVincitaMassima)

            elif self.chiusura < self.minimi[-1]:
                self.prezzoPerditaMassima = self.closePrice + self.p.perditaMassima
                self.prezzoVincitaMassima = self.closePrice - self.p.vincitaMassima
                self.sell_bracket(size=60, stopprice=self.prezzoPerditaMassima, limitprice=self.prezzoVincitaMassima)
