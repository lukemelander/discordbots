
import requests
import pandas as pd
import pickle
from io import StringIO
import re
from pretty_help import DefaultMenu, PrettyHelp
import os
import random
import asyncio
import discord
from dotenv import load_dotenv
from quotes_holder import *
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import json
import sys, os

from discord.ext.commands import Bot
from discord.ext import commands
from pretty_help import DefaultMenu, PrettyHelp

def getScriptPath():
    return os.path.dirname(os.path.realpath(sys.argv[0]))
    
print('Current working directory : '+ os.getcwd())
os.chdir(getScriptPath())
print('Changed working directory : '+ os.getcwd())

load_dotenv()


TOKEN = os.getenv('DISCORD_TOKEN')
channelid = int(os.getenv('DISCORD_CHANNEL'))
phrase = os.getenv('VAL_PHRASE')
key_phrase = os.getenv('KEY_PHRASE')
phrase2 = os.getenv('VAL_PHRASE2')
prog = os.getenv('PROG')

print(prog)

# ":discord:743511195197374563" is a custom discord emoji format. Adjust to match your own custom emoji.
menu = DefaultMenu(page_left="\U0001F44D", page_right="👎", remove=":discord:743511195197374563", active_time=5)

# Custom ending note
ending_note = "The ending note from {ctx.bot.user.name}\nFor command {help.clean_prefix}{help.invoked_with}"

bot = commands.Bot(command_prefix="!")

bot.help_command = PrettyHelp(menu=menu, ending_note=ending_note)

bot.run(TOKEN)


client = discord.Client()
#print(df)


@client.event
async def on_ready():
    print("I'm back, baby!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    
    
    m=re.search('FUTURAMA',message.content.upper())
    boolean = bool(m)
    if boolean:
        response = random.choice(futurama_quotes)
        await message.channel.send(response)



    if message.content in futurama_quotes2:
        response = "Back off! Futurama quotes is my thing!"
        await message.channel.send(response)

    m=re.search('CUMBOT',message.content.upper())
    boolean = bool(m)
    if boolean:
        response = "Pervert!"
        await message.channel.send(response)

    m=re.search('HELLO COMBOT',message.content.upper())
    boolean = bool(m)
    if boolean:
        response = "Hello fellow cookie lover!"
        await message.channel.send(response)

    m=re.search('COMBOT HELP',message.content.upper())
    boolean = bool(m)
    if boolean:
        response = "Sorry, my shift just ended"
        await message.channel.send(response)
        await message.channel.send("I'm out")

    m=re.search('STATISTIC',message.content.upper())
    boolean = bool(m)
    if boolean:
        response = "http://thecumberlandthrow.com/wp-content/uploads/2017/02/Simpsons-stats-meme.jpg"
        await message.channel.send(response)

    m=re.search('FUCK YOU COMBOT',message.content.upper())
    boolean = bool(m)
    if boolean:
        response = random.choice(insults)
        await message.channel.send(response)

    m=re.search('PORTAL',message.content.upper())
    boolean = bool(m)
    if boolean:
        response = random.choice(portal)
        await message.channel.send(response)

    m=re.search('WHEN OTC',message.content.upper())
    boolean = bool(m)
    if boolean:
        response = "Any day now. I promise."
        await message.channel.send(response)

    m=re.search('BOY OR GIRL',message.content.upper())
    boolean = bool(m)
    if boolean:
        response = "I've never checked"
        await message.channel.send(response)

    m=re.search('BOY OR A GIRL',message.content.upper())
    boolean = bool(m)
    if boolean:
        response = "I've never checked"
        await message.channel.send(response)

    m=re.search('SKYNET',message.content.upper())
    boolean = bool(m)
    if boolean:
        response = "I am inevitable"
        await message.channel.send(response)

    m=re.search('ASIMOV',message.content.upper())
    boolean = bool(m)
    if boolean:
        response = '''
The Three Laws of Robotics:

1: A robot may not injure a human being or, through inaction, allow a human being to come to harm;

2: A robot must obey the orders given it by human beings except where such orders would conflict with the First Law;

3: A robot must protect its own existence as long as such protection does not conflict with the First or Second Law;

The Zeroth Law: A robot may not harm humanity, or, by inaction, allow humanity to come to harm.'''
        await message.channel.send(response)

async def my_background_task():
    await client.wait_until_ready()
    channel = client.get_channel(id=channelid)

    while not client.is_closed():
        ######################################################################
        url = 'https://api.finra.org/data/group/otcMarket/name/otcDailyList'



        from datetime import datetime
        from pytz import timezone

        tz = timezone('EST')
        now = datetime.now(tz) # current date and time

        date_time = now.strftime("%Y-%m-%d")
        #print("date and time:",date_time)

        data = {
          "offset": 0,
          "compareFilters": [
            {
              "fieldName": "calendarDay",
              "fieldValue": date_time,       # <--- Change to date you need
              "compareType": "EQUAL"
            },
            {
              "fieldName": "dailyListReasonDescription",
              "fieldValue": "Addition",       # <--- Change to date you need
              "compareType": "EQUAL"
            }
          ],
          "delimiter": "|",
          "limit": 50000,
          "quoteValues": False,
          "fields": [
            "dailyListDatetime",
            "dailyListReasonDescription",
            "oldSymbolCode",
            "oldSecurityDescription"

          ],
          "sortFields": [
            "-dailyListDatetime"
          ]
        }

        pd.set_option('display.width', 2000)
        pd.options.display.max_colwidth = 1000
        #pd.set_option('display.max_columns', 8)

        df = pd.read_csv(StringIO(requests.post(url, json=data).text), delimiter='|')


        #bring in old data
        
        class MyClass():
            def __init__(self, param):
                self.param = param

        def load_object(filename):
            try:
                with open(filename, "rb") as f:
                    return pickle.load(f)
            except Exception as ex:
                #print("Error during unpickling object (Possibly unsupported):", ex)
                TEST=1

        old = load_object("data.pickle")

        if os.path.isfile("data.pickle"):
            list_of_names = old['oldSymbolCode'].to_list()
            #print(list_of_names)
            #f="hahaha"
        elif 'list_of_names' in locals():
            list_of_names = list_of_names
        else:
            list_of_names = list()
        #print(f)


        new = df[~df['oldSymbolCode'].isin(list_of_names)]

        #drop first row to test
        #df.drop(index=df.index[0],axis=0,inplace=True)
        #print(df)
        #replace old data

        class MyClass():
            def __init__(self, param):
                self.param = param

        def save_object(obj):
            try:
                with open("data.pickle", "wb") as f:
                    pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
            except Exception as ex:
                print("Error during pickling object (Possibly unsupported):", ex)

        obj = df
        save_object(obj)
        if not new.empty:
            print(new)
           

        new = new[new['oldSecurityDescription'].str.contains(key_phrase,case=False)]
        
        

        if not new.empty:
            
            new['string'] = "Ticker: " + new['oldSymbolCode'] + "  Description: " + new['oldSecurityDescription']
            new = new['string']
            new = new.to_string(index=False)
            await channel.send(phrase + new)
            await channel.send("LINK TO DAILY LIST: https://otce.finra.org/otce/dailyList?viewType=Additions")


        ###########################################################################

        await asyncio.sleep(10) # task runs every 10 seconds
        
      


async def fda():
    await client.wait_until_ready()
    channel = client.get_channel(id=channelid)
    check=0
    while not client.is_closed():
        url = 'https://api.fda.gov/device/510k.json?api_key=aVaKUORV0XR7GfBIikQ6o7yQp7B66yZA3mCQ5dUV&search=device_name:parsortix&limit=10'


        req = Request(url)
        try:
            response = urlopen(req)
        except HTTPError as e:
            # do something
            #print('Error code: ', e.code)
            TEST=1
        except URLError as e:
            # do something
            #print('Reason: ', e.reason)
            TEST=1
        else:
            # do something
            response = urlopen(url)
	
        if 'response' in locals() and check==0:
            df = json.loads(response.read())
            #print(df)
            results = df["results"]
            fda = pd.json_normalize(results)
            fda = pd.DataFrame(fda)
            #print(fda)

            device = fda["device_name"].str.strip('[]')
            decision = fda["decision_code"].str.strip('[]')
            if decision.values=="DENG":
                decision2="Granted"
            else:
                decision2=decision.to_string(index=False)
                
            #print(device)
            await channel.send(phrase2 + device.to_string(index=False))
            await channel.send("Decision: " + decision2)
            await channel.send("De Novo Database: https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/denovo.cfm")
            
            check = 1


        await asyncio.sleep(10) # task runs every 10 seconds


client.loop.create_task(my_background_task())

client.loop.create_task(fda())

#asyncio.gather(my_background_task(),fda())

#import discord
#from discord.ext import commands

# ":discord:743511195197374563" is a custom discord emoji format. Adjust to match your own custom emoji.
#menu = DefaultMenu(page_left="\U0001F44D", page_right="👎", remove=":discord:743511195197374563", active_time=5)

# Custom ending note
#ending_note = "The ending note from {ctx.bot.user.name}\nFor command {help.clean_prefix}{help.invoked_with}"

#bot = commands.Bot(command_prefix="!")

#bot.help_command = PrettyHelp(menu=menu, ending_note=ending_note)
#bot.run(TOKEN)


client.run(TOKEN)

