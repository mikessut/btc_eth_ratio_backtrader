import backtrader as bt
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

    #def notify_order(self, order):
    #    if order.status == order.Completed:
    #        print("****Order notify:", order)
        

    def next(self):
        # Simply log the closing price of the series from the reference
        #self.log('Close, %.2f' % self.dataclose[0])
        #self.log(f"BTC: {self.btc[0]} ; ETH: {self.eth[0]} {len(self.btc)}")
        #self.log(self.datas[0][0])
        entry_threshold = 1
        trade_amount = 10000

        if self.signal == 0:
            if self.myind.z > entry_threshold:
                self.log(f"ENTRY LONG b: {self.btc[0]} e: {self.eth[0]}")
                # import pdb; pdb.set_trace()
                self.buy(self.btc, size=trade_amount / self.btc[0])
                self.sell(self.eth, size=trade_amount / self.eth[0])
                self.signal = 1
            elif self.myind.z < -entry_threshold:
                self.log(f"ENTRY LONG b: {self.btc[0]} e: {self.eth[0]}")
                # import pdb; pdb.set_trace()
                self.sell(self.btc, size=trade_amount / self.btc[0])
                self.buy(self.eth, size=trade_amount / self.eth[0])
                self.signal = -1
        elif self.signal == 1:
            if self.myind.z < 0:
                self.log("CLOSE LONG")
                self.close(self.btc)
                self.close(self.eth)
                self.signal = 0
        elif self.signal == -1:
            if self.myind.z > 0:
                self.log("CLOSE SHORT")
                self.close(self.btc)
                self.close(self.eth)
                self.signal = 0


if __name__ == '__main__':

    btc = pd.read_pickle('BTC.pd')
    eth = pd.read_pickle('ETH.pd')

    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)
    cerebro.adddata(btfeeds.PandasData(dataname=btc))
    cerebro.adddata(btfeeds.PandasData(dataname=eth))

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    results = cerebro.run()

    ind = results[0].myind.z.array

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()