import json
import requests
from lxml import html

### Generic helper functions

def ConvertListToDict(a):
    it = iter(a)
    res_dct = dict(zip(it, it))
    return res_dct

### Specific helper functions

def determine_option(req, op):
    if op == 'call':
         req["calls"] = True
         req["puts"] = False
    elif op == 'put':
        req["calls"] = False
        req["puts"] = True
    else:
        print('Bad option please try again')
    return req

def determine_diff_price(req, key, value):
    if key == 'diff':
        req["max-diff"] = int(value)
    return req

def determine_order(req, key, value):
    if key == 'asc':
        if value == 'iv':
            req["order-by"] = 'iv_asc'
        elif value == 'expiry':
            req["order-by"] = 'e_asc'
        elif value == 'price':
            req["order-by"] = 'lp_asc'
    elif key == 'desc':
        if value == 'iv':
            req["order-by"] = 'iv_desc'
        elif value == 'expiry':
            req["order-by"] = 'e_desc'
        elif value == 'price':
            req["order-by"] = 'lp_desc'
    return req 

### Functions

def transform_input(msg):

    request = {
        "etf": False, # REQUIRED
        "stock": True, # REQUIRED
        "tickers": 'spce', # any ticker
        "exclude": False,   # use this ticker for search
        "max-diff": 25, # percentage diff from current stock price for strike price
        "itm": True, # REQUIRED
        "otm": True, # REQUIRED
        "calls": True, 
        "puts": False,
        "order-by": 'lp_asc', # desc expir => :e_desc, asc expiry => e_asc, desc iv => iv_desc, asc iv => iv_asc, desc price => lp_desc, asc price => lp_asc
        "active": True
    }

    # print("msg: ", msg)
    input = msg.split()
    # print("input: ", input)

    if len(input) == 3:

        ticker = input[1]
        option = input[2]

        request["tickers"] = ticker
        request = determine_option(request, option)

    elif len(input) > 3:
        
        ticker = input[1]
        option = input[2]
        params = ConvertListToDict(input[3:])

        request["tickers"] = ticker
        request = determine_option(request, option)

        for key, value in params.items():
            # print("key: ", key, "   value: ", value)
            request = determine_diff_price(request, key, value)
            request = determine_order(request, key, value)

    return request


def send_request(req):

    url = "https://api.syncretism.io/ops"
    # More parameters for user input are at https://ops.syncretism.io/api.html

    resp = requests.get(url=url, data=json.dumps(req), headers= {'Content-Type': 'application/json'})
    data = resp.json()[:5]

    return data