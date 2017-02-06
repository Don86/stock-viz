import numpy as np

"""Misc finance calculation functions."""

def simple_return(current, purchase):
    r = (current - purchase)/purchase
    return r

def annualized_return(r, n):
    """Computes the annualized return.
    This computes an annual uniform return, R, given simple return r,
    such that an asset with return R would yield the same value
    after n years.

    Params
    ------
    r: simple return of an asset, float.
    n: no. of years the asset was held, int.

    Returns
    -------
    R: annualized return.
    """
    R = ((1+r)**(1/n)) - 1
    return R


def moving_average(n_period):
    """Compute an n_period moving average of an input array

    Params
    ------
    arr: array, type float. A time series of stock values.
    We assume that the most recent stock value is arr[0].
    n_period: the number of periods to take a moving average over.

    Returns
    -------
    ma: array, type float. A time series of the MA of arr, of length
    len(arr) - n_period
    """
    ma = []
    for i in range(len(arr)-n_period+1):
        window = np.average(arr[i:i+n_period])
        ma.append(window)

    return np.array(ma)


def pull_data_subset(df, t0):
    """
    SEEMS LIKE AN IO FUNCTION; SHIFT TO AN IO LIBRARY
    Pulls the dates and series of prices from dataframe df,
    starting from t0 to the most recent date in df.

    Params
    ------
    df: original DataReader dataframe
    t0: date to pull data from

    Returns
    -------
    df1: dataframe subset, starting from given date t0
    S_data: array. Closing prices starting from date t0.
    S_dates: array. Dates information starting from date t0.

    MOVE TO IO?
    """
    df1 = df.loc[df['Date'] == t0]
    t0_idx = df.loc[df['Date'] == t0].index[0]
    df1 = df.iloc[t0_idx:]
    S_data = np.array(df1['Close'])
    S_dates = np.array(df1['Date'])

    return df1, S_data, S_dates
