import discord
from discord.ext import commands, tasks
from datetime import date, datetime
import yfinance
import os
import random
import sched,time
import fun
import pandas as pd
import asyncio
import calendar
import alpaca_trade_api as tradeapi
client=discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  #channel = client.get_channel(858115001155846165)
  #await channel.send("I'm doing this unprompted!")

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
#Admin Commands
  if msg.startswith('MB help'):
    mout = '```'
    mout += 'Listing all Moistbot commands'
    mout +='\n--MB printphrases= print all bot message/reply exchanges'
    mout +='\n--MB addphrase \\msg\\reply = add new msg\\reply exchange to bot '
    mout +='\n--MB removephrase \msg = remove msg\\reply exchange from bot'
    mout +='\n--MB resetphrases = reset msg\\reply exchanges to defaults'
    mout +='\n--MB printmemes= print all meme triggers'
    mout +='\n--MB addmeme \\msg\\meme reply = add new msg\\meme reply exchange to bot '
    mout +='\n--MB removememe \msg = remove msg\\meme reply exchange from bot'
    mout +='\n--MB resetmemes = reset msg\\meme reply exchanges to defaults'
    mout +='\n--MB printwatch= print watchlist and most recent price'
    mout +='\n--MB addwatch \\TICK = add ticker to group watchlist'
    mout +='\n--MB removewatch \\TICK = remove ticker from group watchlist'
    mout +='```'
    await message.channel.send(mout)

  #Add msg/reply to phrase list
  if msg.startswith('MB addphrase'):
    try:
     phrase = msg.split("\\",2)
     await message.channel.send('"'+phrase[1]+'"'+' '+'"'+phrase[2]+'"')
     fun.fun_msg.append(phrase[1])
     fun.fun_reply.append(phrase[2])
     await message.channel.send('Phrase added')
     f = open('.phrases.txt','w')
     i = 0
     for x in fun.fun_msg:
       f.write(fun.fun_msg[i]+'\\'+fun.fun_reply[i]+'\n')
       i = i+1
    except IndexError:
      await message.channel.send('Format is: M addphrase \\trigger\\response')


  #Print all phrases
  if msg.startswith('MB printphrases'):
    i = 0
    mout = ' '
    await message.channel.send('[All message and reply combinations]')
    for x in fun.fun_msg:
      mout += '--[' + fun.fun_msg[i] + ' | ' + fun.fun_reply[i]+']' + ' \n'
      i = i+1
    await message.channel.send(mout)
 
  #Remove msg/reply from phraselist
  phrase = msg.split("\\",1)
  if phrase[0] == 'MB removephrase ':
    try:
     i = 0
     for x in fun.fun_msg:
       if phrase[1] == fun.fun_msg[i]:
         fun.fun_msg.pop(i)
         fun.fun_reply.pop(i)
         await message.channel.send('Phrase removed')
       i=i+1
     f = open('.phrases.txt','w')
     i = 0
     for x in fun.fun_msg:
       f.write(fun.fun_msg[i]+'\\'+fun.fun_reply[i]+'\n')
       i = i+1
    except IndexError:
      await message.channel.send('Format is: MB removephrase \\trigger\\reply')

  #Reset all phrases to defaults
  if msg.startswith('MB resetphrases'):
      f = open('.phrases.txt','r')
      phraseres = f.readlines()
      fun.fun_msg.clear()
      fun.fun_reply.clear()
      i=0
      for x in phraseres:
        phrase = phraseres[i].split('\\',2)
        phrase[1] = phrase[1].strip('\n')
        fun.fun_msg.append(phrase[0])
        fun.fun_reply.append(phrase[1])
        i = i+1
      await message.channel.send('Phrases reinitialized from archive')

  #Print all memes
  if msg.startswith('MB printmemes'):
    i = 0
    mout = ' '
    sortmsg = fun.fun_msgm
    sortmsg.sort()
    await message.channel.send('[All message and meme reply combinations]')
    for x in fun.fun_msgm:
      #mout += '--[' + fun.fun_msgm[i] + ']' + ' \n'
      mout += '--['+sortmsg[i]+']'+' \n'
      i = i+1
    await message.channel.send(mout)
    f = open('.memes.txt','r')
    memeres = f.readlines()
    fun.fun_msgm.clear()
    fun.fun_meme.clear()
    i=0
    for x in memeres:
      phrase = memeres[i].split('\\',2)
      phrase[1] = phrase[1].strip('\n')
      fun.fun_msgm.append(phrase[0])
      fun.fun_meme.append(phrase[1])
      i = i+1
  
  #Add image meme
  if msg.startswith('MB addmeme'):
     try:
      phrase = msg.split("\\",2)
      await message.channel.send('"'+phrase[1]+'"'+' '+'"'+phrase[2]+'"')
      fun.fun_msgm.append(phrase[1])
      fun.fun_meme.append(phrase[2])
      await message.channel.send('Meme reply added')
      f = open('.memes.txt','w')
      i = 0
      for x in fun.fun_msgm:
        f.write(fun.fun_msgm[i]+'\\'+fun.fun_meme[i]+'\n')
        i = i+1
     except IndexError:
      await message.channel.send('Format is: MB addmeme \\trigger\\meme link')
    
 
  #Remove image meme
  phrase = msg.split("\\",1)
  if phrase[0] == 'MB removememe ':
    try:
     i = 0
     for x in fun.fun_msgm:
       if phrase[1] == fun.fun_msgm[i]:
         fun.fun_msgm.pop(i)
         fun.fun_meme.pop(i)
         await message.channel.send('Meme reply removed')
       i=i+1
     f = open('.memes.txt','w')
     i = 0
     for x in fun.fun_msgm:
       f.write(fun.fun_msgm[i]+'\\'+fun.fun_meme[i]+'\n')
       i = i+1
    except IndexError:
      await message.channel.send('Format is: MB removememe \\trigger')

  #Reset all memes to defaults
  if msg.startswith('MB resetmemes'):
      f = open('.memes.txt','r')
      memeres = f.readlines()
      fun.fun_msgm.clear()
      fun.fun_meme.clear()
      i=0
      for x in memeres:
        phrase = memeres[i].split('\\',2)
        phrase[1] = phrase[1].strip('\n')
        fun.fun_msgm.append(phrase[0])
        fun.fun_meme.append(phrase[1])
        i = i+1
      await message.channel.send('Memes reinitialized from archive')

  #Add to watchlist
  if msg.startswith('MB addwatch'):
    try:
     phrase = msg.split('\\',2)
     fun.watchlist.append(phrase[1])
     await message.channel.send(phrase[1]+' added to group watchlist')
     fun.watchlist.sort()
     f = open('.watch.txt','w')
     i = 0
     for x in fun.watchlist:
       f.write(fun.watchlist[i]+'\n')
       i = i+1

    except IndexError:
     await message.channel.send('Format is: MB addwatch \\TICK')

  #Remove from watchlist
  if msg.startswith('MB removewatch'):
     phrase = msg.split('\\',2)

     i = 0
     for x in fun.watchlist:
      try:
       if phrase[1] == fun.watchlist[i]:
         fun.watchlist.pop(i)
         await message.channel.send(phrase[1]+' removed from group watchlist')
         fun.watchlist.sort()
         f = open('.watch.txt','w')
         j = 0
         for x in fun.watchlist:
           f.write(fun.watchlist[j]+'\n')
           j = j+1
       i=i+1

      except IndexError:
       await message.channel.send('Format is: MB removewatch \\TICK')
      
  #Print watchlist
  if msg.startswith('MB printwatch'):
    async with message.channel.typing():
     f = open('.oauth.alpaca','r')
     alpaca = f.readlines()
     usr_id = alpaca[0].strip('\n')
     usr_scrt = alpaca[1].strip('\n')
     base_url = 'https://paper-api.alpaca.markets'


     api = tradeapi.REST(key_id=usr_id,secret_key=usr_scrt,base_url=base_url,api_version='v2')

     i = 0
     mout = '``` \n'
     mout += 'Cookie Club Watchlist \n'
     mout += '   Ticker   Price   [%change]  % Vol Change\n'
     for x in fun.watchlist:
       try:
          name=x
          data = api.get_barset(name, 'day', limit=2)._raw
          df = pd.DataFrame(data=data)

          close1 = df[name][1]['c']
          close0 = df[name][0]['c']
          vol1 = df[name][1]['v']
          vol0 = df[name][0]['v']

          price = str(close1)

          chan = 100.0*(close1-close0)/close0
          chang = ['{:g}'.format(float('{:.3g}'.format(chan)))]
          change = '['+str(chang[0])+'%]   '

          pvol = 100.0*(vol1-vol0)/vol0
          if pvol >= 0.0:
            pvol = ['{:g}'.format(float('{:.5g}'.format(pvol)))]
            pvol1 = '+'+str(pvol[0])
          else:
            pvol = ['{:g}'.format(float('{:.5g}'.format(pvol)))]
            pvol1 = str(pvol[0])


       except:
         price = '-----'
         change = '-----'
         pvol1 = '-----'
       price = price.ljust(8)
       change = change.ljust(12)
       mout += '   '+fun.watchlist[i].ljust(5) + '|   $'+price+change+pvol1+ '%'+' \n'
       i = i+1
     mout += '```'
     await message.channel.send(mout)
    

  #Reset all phrases to defaults
  if msg.startswith('MB resetwatch'):
      f = open('.watch.txt','r')
      watchres = f.readlines()
      fun.watchlist.clear()
      i=0
      for x in watchres:
        watchres[i] = watchres[i].strip('\n')
        fun.watchlist.append(watchres[i])
        i = i+1
      await message.channel.send('Watchlist reinitialized from archive')

  #Change Daily Update Time
  if msg.startswith('MB changeupdatetime'):
      phrase = msg.split('\\',2)
      update_time = phrase[1]
      f = open('.upt.txt','w')
      f.write(update_time)
      f.close()
      await message.channel.send('Daily Update Time changed to: '+update_time)

#Action Commands
  #Reply to keyphrase with keyreply    
  i = 0
  for x in fun.fun_msg:
    phrase = ''.join(filter(str.isalnum,msg))
    xf = ''.join(filter(str.isalnum,x))
    phrase = phrase.lower()
    xf = xf.lower()
    if phrase.startswith(xf):
        await message.channel.send(fun.fun_reply[i])
    i=i+1


  #Reply to keyphrase with keyreply
  i = 0
  for x in fun.fun_msgm:
    phrase = ''.join(filter(str.isalnum,msg))
    xf = ''.join(filter(str.isalnum,x))
    phrase = phrase.lower()
    xf = xf.lower()
    if phrase.startswith(xf):
      embed = discord.Embed(color=0x00ff00) #creates embed
      embed.set_image(url=fun.fun_meme[i])
      await message.channel.send(embed=embed)
    i=i+1


#
##Send Watchlist Update
#async def testloop():
#  await client.wait_until_ready()
#  channel = client.get_channel(856760108083052585)
#  while not client.is_closed():
#    date_val = date.today().weekday()
#    if date_val < 6:
#      f = open('.upt.txt','r')
#      upt = f.readlines()
#      f.close()
#      now = datetime.now()
#      currentt = now.strftime("%H:%M")
#      if currentt == upt[0]:
#        #i = 0
#        #mout = '``` \n'
#        #mout += 'Cookie Club Watchlist Daily Update\n'
#        #mout += '\tTicker\tPrice   [%change]\t% Vol Change\n'
#        #for x in fun.watchlist:
#        #  try:
#        #    ticker = yfinance.Ticker(fun.watchlist[i])
#        #    price = str(ticker.info['currentPrice'])
#        #    chan = 100.0*(ticker.info['currentPrice']-ticker.info['previousClose'])/ticker.info['previousClose']
#        #    chang = ['{:g}'.format(float('{:.3g}'.format(chan)))]
#        #    hist = ticker.history(period="1wk",interval="1d")
#        #    phrase = str(hist['Volume'].tail(2))
#        #    phrase1 = phrase.split('    ',3)
#        #    vol1 = phrase1[1].split('\n',2)
#        #    vol2 = phrase1[2].split('\n',2)
#        #    pvol = 100.0*(int(vol2[0])-int(vol1[0]))/int(vol1[0])
#        #    change = str(chang[0])
#        #    if pvol >= 0.0:
#        #      pvol = ['{:g}'.format(float('{:.5g}'.format(pvol)))]
#        #      pvol1 = '+'+str(pvol[0])
#        #    else:
#        #      pvol = ['{:g}'.format(float('{:.5g}'.format(pvol)))]
#        #      pvol1 = '-'+str(abs(pvol[0]))
#        #  except:
#        #    price = 'null'
#        #    change= 'null'
#        #    pvol1 = 'null'
#        #  mout += '\t'+fun.watchlist[i] + ' |\t$'+price+'  ['+change+'%] '+'\t' +pvol1+ '%'+' \n'
#        #  i = i+1
#        #mout += '```'
#        #await channel.send(mout) 
#        i = 0
#        mout = '``` \n'
#        mout += 'Cookie Club Watchlist \n'
#        mout += '   Ticker   Price   [%change]  % Vol Change\n'
#        for x in fun.watchlist:
#          try:
#            ticker = yfinance.Ticker(fun.watchlist[i])
#            price = str(ticker.info['currentPrice'])
#            chan = 100.0*(ticker.info['currentPrice']-ticker.info['previousClose'])/ticker.info['previousClose']
#            chang = ['{:g}'.format(float('{:.3g}'.format(chan)))]
#            hist = ticker.history(period="1wk",interval="1d")
#            phrase = str(hist['Volume'].tail(2))
#            phrase1 = phrase.split('    ',3)
#            vol1 = phrase1[1].split('\n',2)
#            vol2 = phrase1[2].split('\n',2)
#            pvol = 100.0*(int(vol2[0])-int(vol1[0]))/int(vol1[0])
#            change = str(chang[0])
#            if pvol >= 0.0:
#              pvol = ['{:g}'.format(float('{:.5g}'.format(pvol)))]
#              pvol1 = '+'+str(pvol[0])
#            else:
#              pvol = ['{:g}'.format(float('{:.5g}'.format(pvol)))]
#              pvol1 = '-'+str(abs(pvol[0]))
#          except:
#            price = '-----'
#            change = '-----'
#            pvol1 = '-----'
#          price = price.ljust(8)
#          change = '['+change+'%]'
#          change = change.ljust(11)
#          mout += '   '+fun.watchlist[i].ljust(5) + '|   $'+price+change+pvol1+ '%'+' \n'
#          i = i+1
#        mout += 'If some are blank, it\'s because of the trash yfinance API'
#        mout += '```'
#        await message.channel.send(mout)
#        await asyncio.sleep(100)
#    await asyncio.sleep(10)
#
#client.loop.create_task(testloop())

client.run(os.getenv('TOKEN'))
