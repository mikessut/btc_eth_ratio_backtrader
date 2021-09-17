## Requirements
    
- Python 3.8
- TA-Lib 
    
## Installation
    
First install TA-Lib C++ library (see https://ta-lib.org/hdr_dw.html), then:

        pip3 install -r requirements.txt

## Notes

As you can tell, it took a fair amount of debug to figure out backtrader. Seems
to sort of work and I think supports the work we were looking at previously.

Had to modify `.\Lib\site-packages\backtrader\plot\locator.py` to get plotting to work.  
`from matplotlib import warnings` instead of `from matplotlib.dates`

I think the summary would be not fantastic results with the parameters as they
are right now.  You would have done better to just buy BTC and ride out the
volatility?

Backtrader needs matplotlib version 3.2.2 and not the latest one. An exception 
will be thrown otherwise and will prevent generating the final chart.

Note that Pyfolio analyser reports work correctly only inside Jupyter notebooks. 
See https://www.backtrader.com/docu/analyzers/pyfolio/
