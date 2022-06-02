import backtrader as bt


class Strategia(bt.Strategy):
    # input parametri strategia
    params = (
        ('perditaMassima', 1.2),
        ('vincitaMassima', 2.0),
    )

    def next(self):
        # if not open trades
        if self.getposition().size == 0:
            # buy if close is greater high else sell if close lower than low
            if self.data.close > self.data.high[-1]:
                self.buy_bracket(size=60,
                                 stopprice=self.data.close - self.p.perditaMassima,
                                 limitprice=self.data.close + self.p.vincitaMassima)

            elif self.data.close < self.data.low[-1]:
                self.sell_bracket(size=60,
                                  stopprice=self.data.close + self.p.perditaMassima,
                                  limitprice=self.data.close - self.p.vincitaMassima)
