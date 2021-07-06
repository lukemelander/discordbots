import discord
import datetime
import yfinance
import os
import random
import sched,time
import fun
client=discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
#Admin Commands
  if msg.startswith('M help'):
    mout = 'Listing all Moistbot commands'
    mout +='\n--M printphrases= print all bot message/reply exchanges'
    mout +='\n--M addphrase \\msg\\reply = add new msg\\reply exchange to bot '
    mout +='\n--M removephrase \msg = remove msg\\reply exchange from bot'
    mout +='\n--M resetphrases = reset msg\\reply exchanges to defaults'
    mout +='\n--M printmemes= print all meme triggers'
    mout +='\n--M addmeme \\msg\\meme reply = add new msg\\meme reply exchange to bot '
    mout +='\n--M removememe \msg = remove msg\\meme reply exchange from bot'
    mout +='\n--M resetmemes = reset msg\\meme reply exchanges to defaults'
    mout +='\n--M printwatch= print watchlist and most recent price'
    mout +='\n--M addwatch \\TICK = add ticker to group watchlist'
    mout +='\n--M removewatch \\TICK = remove ticker from group watchlist'
    await message.channel.send(mout)

  #Add msg/reply to phrase list
  if msg.startswith('M addphrase'):
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
  if msg.startswith('M printphrases'):
    i = 0
    mout = ' '
    await message.channel.send('[All message and reply combinations]')
    for x in sortmsg:
      mout += '--[' + fun.fun_msg[i] + ' | ' + fun.fun_reply[i]+']' + ' \n'
      i = i+1
    await message.channel.send(mout)
 
  #Remove msg/reply from phraselist
  phrase = msg.split("\\",1)
  if phrase[0] == 'M removephrase ':
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
      await message.channel.send('Format is: M removephrase \\trigger\\reply')

  #Reset all phrases to defaults
  if msg.startswith('M resetphrases'):
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
  if msg.startswith('M printmemes'):
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

  #Add image meme
  if msg.startswith('M addmeme'):
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
      await message.channel.send('Format is: M addmeme \\trigger\\meme link')
  
  #Remove image meme
  phrase = msg.split("\\",1)
  if phrase[0] == 'M removememe ':
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
      await message.channel.send('Format is: M removememe \\trigger')

  #Reset all memes to defaults
  if msg.startswith('M resetmemes'):
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
  if msg.startswith('M addwatch'):
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
     await message.channel.send('Format is: M addwatch \\TICK')

  #Remove from watchlist
  if msg.startswith('M removewatch'):
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
       await message.channel.send('Format is: M removewatch \\TICK')

  #Print watchlist
  if msg.startswith('M printwatch'):
    async with message.channel.typing():
     i = 0
     mout = '[Cookie Club Watchlist] \n'
     for x in fun.watchlist:
       ticker = yfinance.Ticker(fun.watchlist[i])
       price = str(ticker.info['currentPrice'])
       chan = 100.0*(ticker.info['currentPrice']-ticker.info['previousClose'])/ticker.info['previousClose']
       chang = ['{:g}'.format(float('{:.2g}'.format(chan)))]
       change = str(chang[0])
       mout += fun.watchlist[i] + ' -- Price: $'+price+' | '+ '% Change: '+change+'%'+' \n'
       i = i+1
     await message.channel.send(mout)      

  #Reset all phrases to defaults
  if msg.startswith('M resetwatch'):
      f = open('.watch.txt','r')
      watchres = f.readlines()
      fun.watchlist.clear()
      i=0
      for x in watchres:
        watchres[i] = watchres[i].strip('\n')
        fun.watchlist.append(watchres[i])
        i = i+1
      await message.channel.send('Watchlist reinitialized from archive')

#Action Commands
  #Reply to keyphrase with keyreply    
  i = 0
  for x in fun.fun_msg:
    if msg.startswith(x):
        await message.channel.send(fun.fun_reply[i])
    i=i+1

  #Reply to keyphrase with keyreply
  i = 0
  for x in fun.fun_msgm:
    if msg.startswith(x):
      embed = discord.Embed(color=0x00ff00) #creates embed
      embed.set_image(url=fun.fun_meme[i])
      await message.channel.send(embed=embed)
    i=i+1

client.run(os.getenv('TOKEN'))
