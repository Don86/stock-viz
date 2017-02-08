'''This example demonstrates embedding a standalone Bokeh document
into a simple Flask application, with a basic HTML web form.
To view the example, run: python simple.py
in this directory, and navigate to: http://localhost:5000
Flask megatutorial of the basics:
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
'''

from __future__ import print_function

import flask
import sys

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from bokeh.models.widgets import PreText, Select

import pandas as pd
import pandas_datareader.data as web
import datetime as dt
from decimal import Decimal
import numpy as np

app = flask.Flask(__name__)


def nix(val, lst):
    # what's this for?
    return [x for x in lst if x != val]


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


def load_ticker(ticker, start, end):
    """An almost-pointlessly short utility function to scrape ticker data,
    and put it in a pandas df. Will have more features added in future.
    """
    df = web.DataReader(ticker, 'yahoo', start, end)
    df.reset_index(inplace=True,drop=False)
    return df


def getitem(obj, item, default):
    if item not in obj:
        return default
    else:
        return obj[item]

"""Specify some hardcoded params ==================="""
ticker_ls = ['^GSPC', 'GLD', 'BRK.B']
start = dt.datetime(2007, 1, 1)
end = dt.datetime(2016, 12, 31)

ticker = '^GSPC'
df = load_ticker(ticker, start, end)

"""=================== Start ==================="""

@app.route("/")
def stock_profile():
    """ Embeds a stock profile of a selected stock.
    """

    # Grab the inputs arguments from the URL
    args = flask.request.args

    # Does this set up widgets?
    # Get all the form arguments in the url with defaults
    # A bokeh Select widget
    ticker1 = Select(value='^GSPC', options=ticker_ls)
    #_from = int(getitem(args, '_from', 0))
    # to = int(getitem(args, 'to', 10))

    # Pull dates and closing prices from the df as arrays
    S_data = np.array(df['Close'])
    S_dates = np.array(df['Date'])
    S_0 = float(df.head(1)['Close'])  # assuming no slippage
    S_T = float(df.tail(1)['Close'])
    dt = 10
    
    # Compute annualized return
    r = simple_return(S_T, S_0)
    R = round(Decimal(annualized_return(r, dt)),3)
    
    # Create graph
    # source = ColumnDataSource(data=dict(date=[], x=[]))
    # source_static = ColumnDataSource(data=dict(date=[], x=[]))
    tools = 'pan, wheel_zoom, reset, xbox_select'

    fig = figure(title=ticker,
                 plot_width=600,
                 plot_height=400,
                 tools=tools,
                 x_axis_type='datetime',
                 active_drag="xbox_select")
    fig.line(S_dates, S_data)

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script, div = components(fig)

    html = flask.render_template(
        'stockprofile.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
        ticker=ticker,
        R_val = R,
        n_periods = dt
    )

    return encode_utf8(html)


if __name__ == "__main__":
    # print(__doc__)
    app.run(debug=True)
