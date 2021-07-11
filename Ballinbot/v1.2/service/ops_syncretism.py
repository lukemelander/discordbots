import yfinance as yf
import json
import requests

### Generic helper functions

def ConvertListToDict(a):
    it = iter(a)
    res_dct = dict(zip(it, it))
    return res_dct

### Specific helper functions

def determine_ticker(req, t):
    error = ''
    ticker = yf.Ticker(t)
    info = None
    try:
        info = ticker.info
    except:
        error = 'Invalid request - Cannot get info of {}, it probably does not exist'.format(t.upper())
        return req, error

    if info['regularMarketPrice'] == None:
        error = 'Invalid request - Cannot get info of {}'.format(t.upper())

    return req, error

def determine_option(req, op):
    if op == 'call':
         req["calls"] = True
         req["puts"] = False
    elif op == 'put':
        req["calls"] = False
        req["puts"] = True
    return req

def determine_diff_price(req, key, value):
    error = ''
    if isinstance(value, int):
        req["max-diff"] = int(value)
    else:
        error = 'Invalid request - {value} is not a number to determine option strike difference to the current stock value'
    return req, error

def determine_order(req, key, value):
    error = ''
    if key == 'low':
        if value == 'iv':
            req["order-by"] = 'iv_asc'
        elif value == 'expiry':
            req["order-by"] = 'e_asc'
        elif value == 'prem':
            req["order-by"] = 'lp_asc'
        else:
            error = 'Invalid request - Unable to sort by low {value}'
    elif key == 'high':
        if value == 'iv':
            req["order-by"] = 'iv_desc'
        elif value == 'expiry':
            req["order-by"] = 'e_desc'
        elif value == 'prem':
            req["order-by"] = 'lp_desc'
        else:
            error = 'Invalid request - Unable to sort by high {value}'
    return req, error

### Functions

def transform_input(msg):

    request = {
        "etf": False, # REQUIRED
        "stock": True, # REQUIRED
        "tickers": '', # any ticker
        "exclude": False,   # use this ticker for search
        "max-diff": 25, # percentage diff from current stock price for strike price
        "itm": True, # REQUIRED
        "otm": True, # REQUIRED
        "calls": True, 
        "puts": False,
        "order-by": 'lp_asc', # high expir => :e_desc, low expiry => e_asc, high iv => iv_desc, low iv => iv_asc, high prem => lp_desc, low prem => lp_asc
        "active": True
    }

    error = ''
        
    if 'call' in msg or 'put' in msg:
        option = 'call' if 'call' in msg else 'put'
        msg.remove(option)
        request = determine_option(request, option)
    else:
        error = 'Invalid request - call or put not provided'

    if 'diff' in msg:
        param = 'diff'
        diff_from_stock = msg[msg.index(param)+1]
        msg.remove(param)
        msg.remove(diff_from_stock)
        request, error = determine_diff_price(request, param, diff_from_stock)

    if 'low' in msg or 'high' in msg:
        param = 'low' if 'low' in msg else 'high'
        sort_by = msg[msg.index(param)+1]
        msg.remove(param)
        msg.remove(sort_by)
        request, error = determine_order(request, param, sort_by)

    if len(msg) == 1:
        ticker = msg[0]
        msg.remove(ticker)
        request, error = determine_ticker(request, ticker)
    else:
        error = 'Invalid request - please try again or type `O help` for examples'

    return request, error


def send_request(req):

    url = "https://api.syncretism.io/ops"
    # More parameters for user input are at https://ops.syncretism.io/api.html

    resp = requests.get(url=url, data=json.dumps(req), headers= {'Content-Type': 'application/json'})
    data = resp.json()[:5]

    return data