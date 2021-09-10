import backtrader as bt
import backtrader.analyzers as btanalyzers
import pandas as pd
import backtrader.feeds as btfeeds
import numpy as np
import math


class Indicator(bt.Indicator):
    lines = ('z', )
    win_size = 20

    def next(self):
        if len(self) > self.win_size:
            avg = np.mean(self.data.get(size=self.win_size))
            std = np.std(self.data.get(size=self.win_size))
            self.z[0] = (self.data[0] - avg) / std


class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        # import pdb; pdb.set_trace()
        self.btc = self.datas[0]
        self.eth = self.datas[1]
        self.myind = Indicator(self.btc / self.eth)
        self.signal = 0
        self.orders = []

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return
        # import pdb; pdb.set_trace()
        if order.status == order.Canceled:
            self.log('Order Canceled')
        elif order.status == order.Margin:
            self.log('Order margin')
        elif order.status == order.Rejected:
            self.log('Order rejected')
        self.orders.remove(order)
        #self.orders = None
        

    def next(self):
        # Simply log the closing price of the series from the reference
        #self.log('Close, %.2f' % self.dataclose[0])
        #self.log(f"BTC: {self.btc[0]} ; ETH: {self.eth[0]} {len(self.btc)}")
        #self.log(self.datas[0][0])
        entry_threshold = 1
        trade_amount = self.broker.get_cash() * .5

        if len(self.orders) > 0:
            self.log("order pending")
            return

        if self.signal == 0:
            if self.myind.z > entry_threshold:
                self.log(f"ENTRY LONG b: {self.btc[0]} e: {self.eth[0]} z: {self.myind.z[0]}")
                # import pdb; pdb.set_trace()
                self.orders.append(self.buy(self.btc, size=trade_amount / self.btc[0]))
                self.orders.append(self.sell(self.eth, size=trade_amount / self.eth[0]))
                self.signal = 1                
            elif self.myind.z < -entry_threshold:
                self.log(f"ENTRY SHORT b: {self.btc[0]} e: {self.eth[0]} z: {self.myind.z[0]}")
                # import pdb; pdb.set_trace()
                self.orders.append(self.sell(self.btc, size=trade_amount / self.btc[0]))
                self.orders.append(self.buy(self.eth, size=trade_amount / self.eth[0]))
                self.signal = -1
        elif self.signal == 1:
            if self.myind.z < 0:
                self.log("CLOSE LONG")
                self.orders.append(self.close(self.btc))
                self.orders.append(self.close(self.eth))
                self.signal = 0
        elif self.signal == -1:
            if self.myind.z > 0:
                self.log("CLOSE SHORT")
                self.orders.append(self.close(self.btc))
                self.orders.append(self.close(self.eth))
                self.signal = 0


if __name__ == '__main__':

    btc = pd.read_pickle('BTC.pd')  # .iloc[:60]
    eth = pd.read_pickle('ETH.pd')  # .iloc[:60]

    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)
    cerebro.adddata(btfeeds.PandasData(dataname=btc))
    cerebro.adddata(btfeeds.PandasData(dataname=eth))
    cerebro.broker.set_cash(10000)
    cerebro.addanalyzer(btanalyzers.SharpeRatio)
    #cerebro.broker.set_checksubmit(False)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    results = cerebro.run()

    ind = results[0].myind.z.array

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print(f"Sharpe: {results[0].analyzers[0].get_analysis()}")
    cerebro.plot()