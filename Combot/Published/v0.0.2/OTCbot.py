
import requests
import pandas as pd
import pickle
from io import StringIO
import asyncio
from dotenv import load_dotenv
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



bot = commands.Bot(command_prefix="CB ", help_command=PrettyHelp())

bot.load_extension("cogs.maincog")
bot.load_extension("cogs.screener")



# ":discord:743511195197374563" is a custom discord emoji format. Adjust to match your own custom emoji.
menu = DefaultMenu('◀️', '▶️', '❌', active_time=30)

# Custom ending note
#ending_note = "The ending note from {ctx.bot.user.name}\nFor command {help.clean_prefix}{help.invoked_with}"


bot.help_command = PrettyHelp(menu=menu)


#bot = discord.bot()
#print(df)




async def my_background_task():
    await bot.wait_until_ready()
    channel = bot.get_channel(id=channelid)

    while not bot.is_closed():
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

        # sometimes this returns an error for too many queries, so I am just trying it and doing nothing if it fails
        try:
            df = pd.read_csv(StringIO(requests.post(url, json=data).text), delimiter='|')
        except:
            pass
        else:
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

            new2 = new[new['oldSecurityDescription'].str.contains("NFT INVESTMENT",case=False)]

            new = new[new['oldSecurityDescription'].str.contains(key_phrase,case=False)]



            if not new.empty:

                new['string'] = "Ticker: " + new['oldSymbolCode'] + "  Description: " + new['oldSecurityDescription']
                new = new['string']
                new = new.to_string(index=False)
                await channel.send(phrase + new)
                await channel.send("LINK TO DAILY LIST: https://otce.finra.org/otce/dailyList?viewType=Additions")

            if not new2.empty:

                new2['string'] = "Ticker: " + new2['oldSymbolCode'] + "  Description: " + new2['oldSecurityDescription']
                new2 = new2['string']
                new2 = new2.to_string(index=False)
                await channel.send('<@816667086553350144> <@582030582947774474> NFT Investments added to the OTC' + new2)
                await channel.send("LINK TO DAILY LIST: https://otce.finra.org/otce/dailyList?viewType=Additions")

            ###########################################################################

            await asyncio.sleep(60) # task runs every 60 seconds


async def fda():
    await bot.wait_until_ready()
    channel = bot.get_channel(id=channelid)
    check = 0
    while not bot.is_closed():
        url = 'https://api.fda.gov/device/510k.json?api_key=aVaKUORV0XR7GfBIikQ6o7yQp7B66yZA3mCQ5dUV&search=device_name:parsortix&limit=10'
        #url = 'https://api.fda.gov/device/510k.json?api_key=aVaKUORV0XR7GfBIikQ6o7yQp7B66yZA3mCQ5dUV&search=device_name:subacromial&limit=10'

        req = Request(url)
        try:
            response = urlopen(req)
        except HTTPError as e:
            # do something
            # print('Error code: ', e.code)
            TEST = 1
        except URLError as e:
            # do something
            # print('Reason: ', e.reason)
            TEST = 1
        else:
            # do something
            response = urlopen(url)

        if 'response' in locals() and check == 0:
            df = json.loads(response.read())
            # print(df)
            results = df["results"]
            fda = pd.json_normalize(results)
            fda = pd.DataFrame(fda)
            print(fda)

            device = fda["device_name"].str.strip('[]')
            decision = fda["decision_code"].str.strip('[]')
            if decision.values == "DENG":
                decision2 = "Granted"
            else:
                decision2 = decision.to_string(index=False)

            # print(device)
            await channel.send(phrase2 + device.to_string(index=False))
            await channel.send("Decision: " + decision2)
            await channel.send("De Novo Database: https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/denovo.cfm")

            check = 1

        await asyncio.sleep(60)  # task runs every 10 seconds

# @bot.listen('on_message')
# async def stuff(message):
#     msg = message.content
#     if msg.startswith('test'):
#
#
#         mout = '``` \n'
#         mout += 'TEST TEST TEST \n'
#         mout += 'TEST TEST TEST\n'
#         mout += '```'
#         await message.channel.send(mout)


bot.loop.create_task(my_background_task())
bot.loop.create_task(fda())

bot.run(TOKEN)

