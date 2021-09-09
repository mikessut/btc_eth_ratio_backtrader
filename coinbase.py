import datetime
import pandas as pd
import requests


COINBASE_API_URL = 'https://api.pro.coinbase.com/'


def historical(product: str, start: datetime.datetime,
               end: datetime.datetime = None,
               granularity: int = 3600) -> pd.DataFrame:
    """
    :param start: Data start
    :param end: Data end time (datetime)
    granularity: Candle time in seconds must be granularity in [60, 300, 900, 3600, 21600, 86400]
    """
    assert granularity in [60, 300, 900, 3600, 21600, 86400], "Invalid granularity"
    if end is None:
        end = datetime.datetime.now()

    total_seconds = (end - start).total_seconds()
    if (total_seconds / granularity) > 300:
        # requires multiple requests
        df = pd.DataFrame()
        tmp_start = start
        tmp_end = start + datetime.timedelta(seconds=granularity*300)
        while tmp_start < end:
            df = df.append(historical(product, tmp_start, tmp_end, granularity))
            tmp_start += datetime.timedelta(seconds=granularity*300)
            tmp_end = tmp_start + datetime.timedelta(seconds=granularity*300)
        return df
    j = {
        'start': start.isoformat(),
        'end': end.isoformat(),
        'granularity': granularity,
    }
    r = requests.get(COINBASE_API_URL + f'products/{product}/candles',
                     params=j)
    df = pd.DataFrame()
    for row in r.json():
        dt = datetime.datetime.fromtimestamp(row[0])
        df.loc[dt, 'Low'] = row[1]
        df.loc[dt, 'High'] = row[2]
        df.loc[dt, 'Open'] = row[3]
        df.loc[dt, 'Close'] = row[4]
        df.loc[dt, 'Volume'] = row[5]
    df = df.sort_index()
    df = df[~df.index.duplicated()]
    return df
