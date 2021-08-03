import os
import sys
import asyncio
import discord
from dotenv import load_dotenv

from service import ops_syncretism as ops
from service import format_output

load_dotenv()

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content.split()

    if msg[0] == 'O':
        
        print('-------------------------------------------')
        print(message.content)
        msg.remove('O')
        
        async with message.channel.typing():
            await asyncio.sleep(0.5)

            if msg[0].lower() == 'help':
                await format_output.show_help(message.channel)
                return

            request, error = ops.transform_input(msg)
            print(request)

            if error != '':
                print(error)
                await format_output.show_error(error, message.channel)
                return
            
            results = ops.send_request(request)

            await format_output.show_results(results, message.channel)


if len(sys.argv) > 1 and sys.argv[1] == 'dev':
    print('Running [dev] optionsbot')
    client.run(os.getenv('TOKEN_DEV'))
else:
    print('Running [Cookie Club] optionsbot')
    client.run(os.getenv('TOKEN'))