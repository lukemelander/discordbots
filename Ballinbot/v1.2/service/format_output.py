import datetime
import discord

async def show_help(channel):
    desc = '''
`O <ticker> <option> <params>...` in any order

> **<ticker>** - any stock that is currently on the market (verified by yahoo finance)

> **<option>** - `call` or `put`

**<params>** - possible paramters include:
> `diff <number>` - this is the strike difference (%) of the option from the current stock trading value

> `high <iv or expiry or prem>` - sort the results from highest to lowest for IV, Expiration, Premium

> `low <iv or expiry or prem>` - sort the results from lowest to highest for IV, Expiration, Premium

E.g. `O spce call diff 50 low iv` - show me all SPCE calls with strikes within 50\% of the current stock value and sort from lowest to highest IV
    '''

    e = discord.Embed(
        color = 0xeabdff, 
        title = 'Help',
        description = desc
    )
    await channel.send(embed = e)

async def show_error(error, channel):
    e = discord.Embed(
        color = 0xCC0000, 
        title = 'Help', 
        description = error
    )
    await channel.send(embed = e)

async def show_results(results, channel):
    output = '```\n'
    output += ' Expiration  Strike  Premium  IV    OI\n'
    output += '-----------------------------------------\n'

    for res in results:
        
        if res["strike"] < 25.0:
            expiry = str((datetime.datetime.fromtimestamp(res["expiration"]) + datetime.timedelta(days=1)).strftime('%Y-%m-%d')).ljust(12)
            strike = "$" + str("{:.2f}".format(res["strike"])).ljust(7)
        else:
            expiry = str((datetime.datetime.fromtimestamp(res["expiration"]) + datetime.timedelta(days=1)).strftime('%Y-%m-%d')).ljust(13)
            strike = "$" + str("{:.0f}".format(res["strike"])).ljust(6)
        
        last_price = "$" + str("{:.2f}".format(res["lastPrice"])).ljust(7)
        iv = str('%.2f' % res["impliedVolatility"]).ljust(7)
        oi = str(res["volume"])
        # data = (expiry, strike, last_price, iv, oi)
        output += ' ' + expiry + strike + last_price + iv + oi + '\n'
    output += '```'

    e = discord.Embed(
        title = 'Results', 
        description = output
    )
    await channel.send(embed = e)