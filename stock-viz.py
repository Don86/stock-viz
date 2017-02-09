from __future__ import print_function

import flask

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from bokeh.models.widgets import PreText, Select

import pandas_datareader.data as web
import datetime as dt
import numpy as np
from decimal import Decimal


app = flask.Flask(__name__)

""" ====================== All the functions ======================"""
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


def calc_ticker_stats(df):
    """Returns a variety of ticker statistics that I use.
    An encapsulating function."""

    S_data = np.array(df['Close'])
    S_dates = np.array(df['Date'])
    S_0 = float(df.head(1)['Close'])  # assuming no slippage
    S_T = float(df.tail(1)['Close'])

    lgS = []
    for i in range(1, len(S_data)):
        lg_r = S_data[-i] / S_data[-i - 1]
        lgS.append(lg_r)
    lgS = np.array(lgS)

    stats_dict = {'S_data': S_data,
                  'S_dates': S_dates,
                  'S_0': S_0,
                  'S_T': S_T,
                  'lgS': lgS}

    return stats_dict

"""Specify some hardcoded params ==================="""
ticker_ls = ['^GSPC', 'GLD', 'BRK.B', 'FTSE']
start = dt.datetime(2007, 1, 1)
end = dt.datetime(2016, 12, 31)
ticker = '^GSPC'
"""=================== Start ==================="""

@app.route("/")
def index():
    """ landing page which doesn't contain any graph.
    """
    html = flask.render_template('main.html')

    return encode_utf8(html)


@app.route("/<tickername>")
def profile(tickername):
    # scrape data
    df = load_ticker(tickername, start, end)
    src = calc_ticker_stats(df)
    dt = 10
    r = simple_return(src['S_T'], src['S_0'])
    R = round(Decimal(annualized_return(r, dt)), 3)


    # Create graph
    tools = 'pan, wheel_zoom, reset, xbox_select'
    fig_title = tickername + " log returns"

    fig = figure(title=fig_title,
                 plot_width=550,
                 plot_height=300,
                 tools=tools,
                 x_axis_type='datetime',
                 active_drag="xbox_select")
    fig.line(src['S_dates'], src['lgS'])

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()
    script, div = components(fig)

    # render on stockprofile.html
    html = flask.render_template(
        'stockprofile.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
        ticker=ticker,
        R_val=R,
        n_periods=dt,
    )

    return encode_utf8(html)


if __name__ == "__main__":
    # print(__doc__)
    app.run(debug=True)
