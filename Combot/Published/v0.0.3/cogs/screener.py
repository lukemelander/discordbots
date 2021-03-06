import decimal
import re
from decimal import Decimal

import discord
import finviz
import numpy
import pandas as pd
from discord.ext import commands
from itertools import chain

from pandas import to_numeric


class Screeners(commands.Cog, name= 'Screener'):
    """FinViz Screener"""
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name="CB INSIDER [TICKER] [number of entries]", brief='Shows insider trading information \n\nNote: You can replace \'INSIDER\' with \'I\' for short.', description='')
    async def screenhelp1(ctx):
        await ctx.send('CB INSIDER [TICKER]')

    @commands.command(name="CB NEWS [TICKER] [number of entries]", brief='Shows recent news for a ticker. \n\nNote: You can replace \'NEWS\' with \'N\' for short.', description='')
    async def screenhelp2(ctx):
        await ctx.send('CB NEWS [TICKER]')

    @commands.command(name="CB SCREENER FILTER=[FinViz Filters]", brief='Pulls screening data. \n\nNote: Go to finviz.com/screener.ashx, select desired filters, copy/paste filters from bottom of table.', description='')
    async def screenhelp3(ctx):
        await ctx.send('CB SCREENER FILTER=[FinViz Filters]')

    @commands.command(name="CB PT [TICKER] [number of entries] rating", brief='Shows price targets for a ticker. Optional to include ratings.\n', description='')
    async def screenhelp4(ctx):
        await ctx.send('CB PT [TICKER]')


    @commands.Cog.listener()
    async def on_message(self, message):


        if message.author == self.bot.user:
            return

        m = re.search('^CB [INP]', message.content.upper())
        if bool(m):
            msg = message.content.upper()
            ticker = re.compile("\s\S*\s([a-zA-Z]*)").split(msg)[1].lstrip()

            try:
                stock = finviz.get_stock(ticker)
            except:
                mout = "The ticker " + ticker + " does not exist in finviz"
                embed = discord.Embed(title='Error', description=mout, color=0x00ff00)
                await message.channel.send(embed=embed)
                return




        m = re.search('^CB I[NSIDER]?', message.content.upper())
        if bool(m):
            msg = message.content.upper()
            ticker = re.compile("\s\S*\s([a-zA-Z]*)").split(msg)[1].lstrip()
            n=None
            n = re.findall(r'\d+', msg)
            if not n:
                n=50
            else:
                n=int(n[0])
            #print(ticker)
            try:
                response = finviz.get_insider(ticker)
            except:
                mout = "There is no insider data for " + ticker
            else:
                response = pd.json_normalize(response)
                response = pd.DataFrame(response)

                response['Insider Trading'] = response['Insider Trading'].str.slice(0, 22)

                response['Transaction'] = response['Transaction'].astype(str).replace('Option Exercise', 'OE', regex=True)
                response['Insider Trading'] = response['Insider Trading'].astype(str).replace('(?<=\s.{1}).*',"",regex=True)
                response = response[0:n]
                #print(response.columns.values)
                response = response[["Insider Trading", "Date", "Transaction", "#Shares"]]

                mout = '```\n'
                #mout += '             Insider     Date  Trans.   Shares\n'
                response['Insider Trading'] = "" + response['Insider Trading'].astype(str) + "|"
                response['Date'] = response['Date'].astype(str) + "|"
                response['Transaction'] = response['Transaction'].astype(str) + "|"
                response['#Shares'] = response['#Shares'].astype(str)  # + "| "
                # response['Perf Month'] = response['Perf Month'].astype(str)
                mout += response.to_string(index=False, header=False)
                mout += '```'

            embed = discord.Embed(title='Insider Trading', description=mout, color=0x00ff00)
            embed.add_field(name="Legend", value="OE=Options Exercised")
            await message.channel.send(embed=embed)

        m = re.search('^CB N[EWS]?', message.content.upper())
        if bool(m):
            msg = message.content.upper()
            ticker = re.compile("\s\S*\s([a-zA-Z]*)").split(msg)[1].lstrip()
            n=None
            n = re.findall(r'\d+', msg)
            if not n:
                n=10
            else:
                n=int(n[0])
            #print(ticker)

            news = finviz.get_news(ticker)
            #print(news)
            news = list(news)
            news = pd.DataFrame(news, columns=["Date", "News", "URL", "Source"])
            news = news.sort_values('Date',ascending=False)
            news = news[["Date", "News", "Source", "URL"]]
            news["News"] = news["News"].str.lstrip(' ')
            news["URL"] = "[LINK](https://" + news["URL"] + ")"
            response = news[0:n]
            D1 = pd.DataFrame()
            async with message.channel.typing():

                #mout += ' Date   Story   Source\n'
                #D1['start'] = 'a'
                D1['Date'] = ' Date: ' + response['Date']+'\n'
                D1['News'] = ' Story: ' + response['News'] + '\n'
                D1['Source'] = 'Source: ' + response['Source'] + '\n'
                #D1['URL'] = 'URL: ' + response['URL'] + '\n'
                #add this line just to return a blank line
                D1['return'] = ' \n '
                D1 = D1.values.tolist()
                D1 = "".join(ele for sub in D1 for ele in sub)


                mout = '``` \n '
                mout += D1 #.to_string(index=False, header=False)
                mout += '\n```'

                embed = discord.Embed(title='Stock News', description=mout)
                await message.channel.send(embed=embed)



        m = re.search('^CB SCREENER', message.content.upper())
        if bool(m):
            msg = message.content.lower()

            #f = setup_filters(msg)


            msg = msg.replace(":","_")
            #print(msg)

            #set up filters

            if bool(re.search('filters.*=', msg)):
                f = re.compile('screener filters.*=').split(msg)[1].lstrip()
                #print(f)
                f = f.partition(' ')
                #print(f)
            else:
                f=[]



            async with message.channel.typing():

                #filters = ['exch_nasd', 'idx_sp500']
                stock_list = Screener(filters=f, table='Performance', order='price')
                stock_list = pd.json_normalize(stock_list)
                stock_list = pd.DataFrame(stock_list)
                stock_list = stock_list.sort_values('Ticker')
                #print(stock_list)
                response = stock_list[0:100]
                response = response[["Ticker", "Price", "Change", "Volume"]]

                mout = '```\n'
                mout += ' Ticker   Price   Change      Volume\n'
                response['Ticker'] = "  " + response['Ticker'].astype(str)+"| "
                response['Price'] = response['Price'].astype(str) + "| "
                response['Change'] = response['Change'].astype(str) + "| "
                response['Volume'] = response['Volume'].astype(str) #+ "| "
                #response['Perf Month'] = response['Perf Month'].astype(str)
                mout += response.to_string(index=False, header=False)
                mout += '```'
                embed = discord.Embed(title='Stock Screener', description=mout)
                await message.channel.send(embed=embed)


        m = re.search('^CB PT', message.content.upper())
        if bool(m):
            msg = message.content.upper()
            ticker = re.compile("\s\S*\s([a-zA-Z]*)").split(msg)[1].lstrip()
            r = None
            if "rating" in msg.lower():
                r = 1

            n=None
            n = re.findall(r'\d+', msg)
            if not n:
                n=50
            else:
                n=int(n[0])

            #print(ticker)
            #print(n)
            try:
                response = finviz.get_analyst_price_targets(ticker, last_ratings=n)
            except:
                mout = "There is no price target data for " + ticker
            else:
                response = pd.json_normalize(response)
                response = pd.DataFrame(response)

                #print(response)
                tail_dot_rgx = re.compile(r'(?:(\.)|(\.\d*?[1-9]\d*?))0+(?=\b|[^0-9])')
                def remove_tail_dot_zeros(a):
                    return tail_dot_rgx.sub(r'\2', a)

                def fix_target(df):
                    if 'target' not in df and 'target_from' not in df:
                        return "no PT columns in finviz"
                    elif 'target_from' in df and str(df['target_from']) != "nan":
                        return remove_tail_dot_zeros(str(round(df['target_from']))) + '->' + remove_tail_dot_zeros(str(round(df['target_to'])))
                    elif str(df['target']).upper() == "NAN":
                        return "-"
                    else:
                        return remove_tail_dot_zeros(str(round(df['target'], 2)))



                response['target'] = response.apply(fix_target, axis=1)
                #print(response['target'])
                try:
                    response['analyst'] = response['analyst'].str.slice(0, 20)
                except:
                    mout = "There is no price target data for " + ticker
                else:

                    response['rating'] = response['rating'].astype(str).replace('Underperform', 'UP', regex=True)
                    response['rating'] = response['rating'].astype(str).replace('Outperform', 'OP', regex=True)
                    response['rating'] = response['rating'].astype(str).replace('Overweight', 'OW', regex=True)
                    response['rating'] = response['rating'].astype(str).replace('Underweight', 'UW', regex=True)
                    response['rating'] = response['rating'].astype(str).replace('Equal Weight', 'EW', regex=True)
                    response['rating'] = response['rating'].astype(str).replace('Equal-Weight', 'EW', regex=True)
                    response['rating'] = response['rating'].astype(str).replace('Peer Perform', 'PP', regex=True)
                    response['rating'] = response['rating'].astype(str).replace('Sector Perform', 'SP', regex=True)
                    response['rating'] = response['rating'].astype(str).replace('Market Perform', 'MP', regex=True)
                    response['rating'] = response['rating'].astype(str).replace('Neutral', 'N', regex=True)
                    response['rating'] = response['rating'].astype(str).replace('Hold', 'H', regex=True)
                    response['rating'] = response['rating'].astype(str).replace('Buy', 'B', regex=True)
                    response['rating'] = response['rating'].astype(str).replace('Strong B', 'SB', regex=True)
                    response['rating'] = response['rating'].astype(str).replace('Sell', 'S', regex=True)
                    response['rating'] = response['rating'].astype(str).replace('Strong S', 'S', regex=True)
                    response['rating'] = response['rating'].astype(str).replace('In-line', 'IL', regex=True)
                    response['rating'] = response['rating'].astype(str).replace('Inline', 'IL', regex=True)
                    response['rating'] = response['rating'].astype(str).replace('Perform', 'P', regex=True)
                    response['rating'] = response['rating'].astype(str).replace('Positive', '+', regex=True)
                    response['rating'] = response['rating'].astype(str).replace('Negative', '-', regex=True)
                    response['rating'] = response['rating'].astype(str).replace('Mkt P', 'MP', regex=True)
                    response['rating'] = response['rating'].astype(str).replace('Sector Weight', 'SW', regex=True)
                    response['rating'] = response['rating'].astype(str).replace('Sector OP', 'OP', regex=True)
                    response['rating'] = response['rating'].astype(str).replace(' ', '', regex=True)
                    #print(response.columns.values)
                    response = response[["analyst", "date", "rating", "target"]]

                    mout = '```\n'
                    #mout += '             Insider     Date  Trans.   Shares\n'
                    response['analyst'] = "" + response['analyst'].astype(str) + "|"
                    response['date'] = response['date'].astype(str) + "|"
                    response['rating'] = response['rating'].astype(str) + "|"
                    response['target'] = response['target'].astype(str)  # + "| "

                    if r != 1:
                        response = response.drop(["rating"],axis=1)

                    # response['Perf Month'] = response['Perf Month'].astype(str)
                    mout += response.to_string(index=False, header=False)
                    mout += '```'

            embed = discord.Embed(title='Analyst Price Targets', description=mout, color=0x00ff00)
            if r ==1:
                embed.add_field(name="Legend: ", value="- = No PT given \n+ = Positive \n- = Negative \nB = Buy \nEW = Equal Weight \nH = Hold \nIL = In-line \nN = Neutral \nMP = Market Perform \nOP = Outperform \nOW = Overweight \nP = Perform \nPP = Peer Perform \nS = Sell \nSB = Strong Buy \nSP = Sector Perform \nSS = Strong Sell \nSW = Sector Weight \nUP = Underperform \nUW = Underweight")
            else:
                embed.add_field(name="Legend: ", value="- = Likely a rating without a PT")
            await message.channel.send(embed=embed)



def setup(bot):
    bot.add_cog(Screeners(bot))