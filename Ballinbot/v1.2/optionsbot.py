import os
import sys
import datetime

import discord
import asyncio
from dotenv import load_dotenv
from tabulate import tabulate

import ops_syncretism_service as ops

load_dotenv()

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('O '):
        
        async with message.channel.typing():
            await asyncio.sleep(0.5)

            print('-------------------------------------------')
            print(msg)

            request, error = ops.transform_input(msg)

            if error != '':
                print(error)
                embed = discord.Embed(color = 0xCC0000, title = 'Error', description = error)
                await message.channel.send(embed = embed)
                return
            
            results = ops.send_request(request)

            # table = [["expiry", "strike", "premium", "IV", "OI"]]
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

            embed = discord.Embed(title = 'Results', description = output)
            await message.channel.send(embed = embed)


if len(sys.argv) > 1 and sys.argv[1] == 'dev':
    print('Running [dev] optionsbot')
    client.run(os.getenv('TOKEN_DEV'))
else:
    print('Running [Cookie Club] optionsbot')
    client.run(os.getenv('TOKEN'))