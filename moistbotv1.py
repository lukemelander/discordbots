import discord
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
  if msg.startswith('moistbot commands'):
    mout = 'Listing all Moistbot commands'
    mout +='\n--moistbot print phraselist = print all bot message/reply exchanges'
    mout +='\n--moistbot addphrase \msg\\reply = add new msg\\reply exchange to bot '
    mout +='\n--moistbot removephrase \msg = remove msg\\reply exchange from bot'
    mout +='\n--moistbot resetphrases = reset msg\\reply exchanges to defaults'
    mout +='\n--moistbot print memelist = print all meme triggers'
    mout +='\n--moistbot addmeme \msg\\meme reply = add new msg\\meme reply exchange to bot '
    mout +='\n--moistbot removememe \msg = remove msg\\meme reply exchange from bot'
    mout +='\n--moistbot resetmemes = reset msg\\meme reply exchanges to defaults'

    await message.channel.send(mout)

  #Add msg/reply to phrase list
  if msg.startswith('moistbot addphrase'):
    phrase = msg.split("\\",2)
    await message.channel.send('"'+phrase[1]+'"'+' '+'"'+phrase[2]+'"')
    fun.fun_msg.append(phrase[1])
    fun.fun_reply.append(phrase[2])
    await message.channel.send('Phrase added')

  #Print all phrases
  if msg.startswith('moistbot phraselist'):
    i = 0
    mout = ' '
    await message.channel.send('[All message and reply combinations]')
    for x in fun.fun_msg:
      mout += '--[' + fun.fun_msg[i] + ' | ' + fun.fun_reply[i]+']' + ' \n'
      i = i+1
    await message.channel.send(mout)
 
  #Remove msg/reply from phraselist
  phrase = msg.split("\\",1)
  if phrase[0] == 'moistbot removephrase ':
    i = 0
    for x in fun.fun_msg:
      if phrase[1] == fun.fun_msg[i]:
        fun.fun_msg.pop(i)
        fun.fun_reply.pop(i)
        await message.channel.send('Phrase removed')
      i=i+1

  #Reset all phrases to defaults
  if msg.startswith('moistbot resetphrases'):
      fun.fun_msg = list(fun.fun_msg_i)
      fun.fun_reply = list(fun.fun_reply_i)
      await message.channel.send('Phrases reset to defaults')

  #Print all memes
  if msg.startswith('moistbot print memelist'):
    i = 0
    mout = ' '
    await message.channel.send('[All message and meme reply combinations]')
    for x in fun.fun_msgm:
      mout += '--[' + fun.fun_msgm[i] + ']' + ' \n'
      i = i+1
    await message.channel.send(mout)

  #Add image meme
  if msg.startswith('moistbot addmeme'):
      phrase = msg.split("\\",2)
      await message.channel.send('"'+phrase[1]+'"'+' '+'"'+phrase[2]+'"')
      fun.fun_msgm.append(phrase[1])
      fun.fun_meme.append(phrase[2])
      await message.channel.send('Meme reply added')

  #Remove image meme
  phrase = msg.split("\\",1)
  if phrase[0] == 'moistbot removememe ':
    i = 0
    for x in fun.fun_msgm:
      if phrase[1] == fun.fun_msgm[i]:
        fun.fun_msgm.pop(i)
        fun.fun_meme.pop(i)
        await message.channel.send('Meme reply removed')
      i=i+1

  #Reset all memes to defaults
  if msg.startswith('moistbot resetmemes'):
      fun.fun_msgm = list(fun.fun_msgm_i)
      fun.fun_meme = list(fun.fun_meme_i)
      await message.channel.send('Phrases reset to defaults')        

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


  #Reply to message with meme
  if msg.startswith('hindsight' or 'hindsight?'):
    embed = discord.Embed(title="Hindsight?", color=0x00ff00) #creates embed
    file = discord.File("images/hindsight.png", filename="hindsight.png")
    embed.set_image(url="attachment://hindsight.png")
    await message.channel.send(file=file, embed=embed)

client.run(os.getenv('TOKEN'))
