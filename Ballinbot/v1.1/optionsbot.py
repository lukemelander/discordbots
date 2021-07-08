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
                await message.channel.send(error)
                return
            
            results = ops.send_request(request)

            table = [["expiry", "strike", "premium", "IV", "OI"]]

            for res in results:
                data = []
                expiry = datetime.datetime.fromtimestamp(res["expiration"]).strftime('%Y-%m-%d')
                data.append(expiry)
                strike = "$" + str(res["strike"])
                data.append(strike)
                last_price = "$" + str(res["lastPrice"])
                data.append(last_price)
                iv = '%.2f' % res["impliedVolatility"]
                data.append(iv)
                oi = res["volume"]
                data.append(oi)
                table.append(data)
            
            table_output = tabulate(table, headers="firstrow", tablefmt="grid")

            output = """
```
{}
```
            """.format(table_output)

            await message.channel.send(output)


if sys.argv[1] == 'dev':
    print('Running [dev] optionsbot')
    client.run(os.getenv('TOKEN_DEV'))
else:
    print('Running [Cookie Club] optionsbot')
    client.run(os.getenv('TOKEN'))