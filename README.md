
As you can tell, it took a fair amount of debug to figure out backtrader.  Seems
to sort of work and I think supports the work we were looking at previously.

Had to modify `.\Lib\site-packages\backtrader\plot\locator.py` to get plotting to work.  
`from matplotlib import warnings` instead of `from matplotlib.dates`

I think the summary would be not fantastic results with the parameters as they
are right now.  You would have done better to just buy BTC and ride out the
volatility?