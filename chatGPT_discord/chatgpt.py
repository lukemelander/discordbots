import discord
from discord.ext import commands, tasks
import os
import io
import asyncio
import math
import openai

###Reads in the API token to log into the discord bot
#		token needs to be stored in a text file called .oauth.discord
f = open('.oauth.discord','r')
discordT = f.readlines()
Token = discordT[0].strip('\n')
client=discord.Client(intents=discord.Intents.default())
cHist = {}

###Initializing
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


###Loop that checks for new messages
#	if there is a new message, then it reads it's text content
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
  ###AI Text Response
  uname = message.author.name

  f = open('.oauth.openai','r') #   reading in the openai API token to be able to access GPT online library
  openaiT = f.readlines()
  openai.api_key = openaiT[0].strip('\n')

  if msg.startswith('Create'):
    async with message.channel.typing():
       modcheck=openai.Moderation.create(input=msg)
       if modcheck["results"][0]["flagged"] == False:
          resp = openai.Image.create(prompt=msg,n=1,size="1024x1024")
          await message.channel.send(resp['data'][0]['url'])
       else:
          await message.channel.send('Sorry, prompt flagged')
  if msg.startswith('delhistory'):
      cHist[uname] = {}
  else:
    phrase = msg 	#removes call command from message
    resplen = 4000
    if uname in cHist.keys():
       cHist[uname][len(cHist[uname])] = phrase
    else:
       cHist[uname] = {}
       cHist[uname][0] = ''
       cHist[uname][1] = phrase
    inputtext = cHist[uname][0]+'\n'+phrase
    async with message.channel.typing():  #Puts the "bot is typing" thing on discord
      modcheck = openai.Moderation.create(   #Calls the content filter to see if message contains hate/sex/profanity
          input=inputtext
      )
      if modcheck["results"][0]["flagged"] == False:   #If no banned content, continue
         resp = openai.ChatCompletion.create(              #Calls the GPT chat function
           model="gpt-3.5-turbo",
           messages=[{"role":"user","content":inputtext}]
         )
         cHist[uname][len(cHist[uname])] = resp.choices[0].message.content
         await message.channel.send(resp.choices[0].message.content)  #Puts the chatGPT reply in the discrod channel user called it
         text= ' '
         for x in range(1,len(cHist[uname])):
            if x % 2 == 0:
              text = text+cHist[uname][x]
            else:
              text = text+'\n'+cHist[uname][x]
         cHist[uname][0] = text
         if resp["usage"]["prompt_tokens"] > resplen:
            for x in range(1,len(cHist[uname])-1):
                cHist[uname][x]=cHist[uname][x+1]
            del cHist[uname][len(cHist[uname])-1]
            for x in range(1,len(cHist[uname])-1):
                cHist[uname][x]=cHist[uname][x+1]
            del cHist[uname][len(cHist[uname])-1]
      else:
        await message.channel.send("Unable to complete due to flagged content") #if banned content, reply with this
client.run(Token)
