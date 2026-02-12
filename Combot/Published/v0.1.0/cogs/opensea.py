import re
import discord
from discord.ext import commands
import requests
import pandas as pd
import json

class opensea(commands.Cog, name= 'opensea'):
    """Opensea Price Points"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="CB F [collection]", brief='Shows the floor of opensea collection \n (note: cc=cryptocoven can be used as a shortcut)', description='')
    async def screenhelp1(self, ctx):
        await ctx.send('CB F [collection]')


    @commands.Cog.listener()
    async def on_message(self, message):


        if message.author == self.bot.user:
            return






        m = re.search('^CB F[LOOR]?', message.content.upper())
        if bool(m):
            msg = message.content
            collection = re.compile(r"\s\S*\s([a-zA-Z0-9!$* \t\r\n\-]*)").split(msg)[1].lstrip()
            #quote_page = "https://opensea.io/collection/cryptocoven?search[sortBy]=PRICE&search[sortAscending]=true&search[toggles][0]=BUY_NOW&search[priceFilter][symbol]=ETH&search[priceFilter][max]=" + price

            url = "https://api.opensea.io/api/v1/collection/cryptocoven/stats" if (collection.upper() == "CC") \
                else "https://api.opensea.io/api/v1/collection/" + collection + "/stats"
            print(url)


            headers = {"Accept": "application/json"}

            response = requests.request("GET", url, headers=headers)
            try:
                data = json.loads(response.text)

                floor = str(round(data["stats"]["floor_price"],4))

                collections = "Crypto Coven" if collection.upper() == "CC" else collection

                mout = "The current floor price is " + floor + " for " + collections
                embed = discord.Embed(title='Floor Tracker', description=mout, color=0x00ff00)

                await message.channel.send(embed=embed)
            except:
                print("That collection doesn't exist")





        m = re.search('^CB S[TATS]?', message.content.upper())
        if bool(m):
            msg = message.content
            collection = re.compile(r"\s\S*\s([a-zA-Z0-9!$* \t\r\n\-]*)").split(msg)[1].lstrip()
            # quote_page = "https://opensea.io/collection/cryptocoven?search[sortBy]=PRICE&search[sortAscending]=true&search[toggles][0]=BUY_NOW&search[priceFilter][symbol]=ETH&search[priceFilter][max]=" + price

            url = "https://api.opensea.io/api/v1/collection/cryptocoven/stats" if (collection.upper() == "CC") \
                else "https://api.opensea.io/api/v1/collection/" + collection + "/stats"
            print(url)

            headers = {"Accept": "application/json"}

            response = requests.request("GET", url, headers=headers)
            try:
                data = json.loads(response.text)

                floor = str(round(data["stats"]["floor_price"], 4))

                collections = "Crypto Coven" if collection.upper() == "CC" else collection


                mout = '```\n'
                mout += '                 floor: ' + str(round(data["stats"]["floor_price"], 4)) + '\n'
                mout += '           1 day sales: ' + str(round(data["stats"]["one_day_sales"], 4)) + '\n'
                mout += '          1 day volume: ' + str(round(data["stats"]["one_day_volume"], 4)) + '\n'
                mout += '       1 day avg price: ' + str(round(data["stats"]["one_day_average_price"], 4)) + '\n'
                mout += '           total sales: ' + str(round(data["stats"]["total_sales"], 4)) + '\n'
                mout += '          total volume: ' + str(round(data["stats"]["total_volume"], 4)) + '\n'
                mout += '            market cap: ' + str(round(data["stats"]["market_cap"], 4)) + '\n'
                mout += 'ownership distribution: ' + \
                       str((round(data["stats"]["num_owners"]/data["stats"]["total_supply"], 4))*100) + '% \n'

                mout += '```'


                embed = discord.Embed(title='NFT Stats Tracker - ' + collections, description=mout, color=0x00ff00)

                await message.channel.send(embed=embed)
            except:
                print("That collection doesn't exist")



async def setup(bot):
    await bot.add_cog(opensea(bot))
