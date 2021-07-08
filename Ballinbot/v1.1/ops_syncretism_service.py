import json
import requests

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
    return req

def determine_diff_price(req, key, value):
    req["max-diff"] = int(value)
    return req

def determine_order(req, key, value):
    if key == 'asc':
        if value == 'iv':
            req["order-by"] = 'iv_asc'
        elif value == 'expiry':
            req["order-by"] = 'e_asc'
        elif value == 'prem':
            req["order-by"] = 'lp_asc'
    elif key == 'desc':
        if value == 'iv':
            req["order-by"] = 'iv_desc'
        elif value == 'expiry':
            req["order-by"] = 'e_desc'
        elif value == 'prem':
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
        "order-by": 'lp_asc', # desc expir => :e_desc, asc expiry => e_asc, desc iv => iv_desc, asc iv => iv_asc, desc prem => lp_desc, asc prem => lp_asc
        "active": True
    }

    error = ''

    input = msg.split()

    if len(input) == 3:

        ticker = input[1]
        request["tickers"] = ticker

        option = input[2]
        if option == 'call' or option == 'put':
            request = determine_option(request, option)
        else:
            error = 'Bad option - not a call or put'
            return request, error

    elif len(input) > 3:
        
        ticker = input[1]
        request["tickers"] = ticker

        option = input[2]
        if option == 'call' or option == 'put':
            request = determine_option(request, option)
        else:
            error = 'Bad option - not a call or put'
            return request, error

        if len(input) % 2 == 0:
            error = 'Bad parameter - incorrect number of paramters'
            return request, error

        params = ConvertListToDict(input[3:])
        for key, value in params.items():
            print("key: ", key, "   value: ", value)
            if key == 'diff':
                request = determine_diff_price(request, key, value)
            elif key == 'asc' or key == 'desc':
                request = determine_order(request, key, value)
            else:
                error = 'Bad parameter - not a diff <int>, asc <iv|prem|expiry>, or desc <iv|prem|expiry>'
                return request, error
    
    else:
        error = 'Invalid request, please try again'
        return request, error

    return request, error


def send_request(req):

    url = "https://api.syncretism.io/ops"
    # More parameters for user input are at https://ops.syncretism.io/api.html

    resp = requests.get(url=url, data=json.dumps(req), headers= {'Content-Type': 'application/json'})
    data = resp.json()[:5]

    return data