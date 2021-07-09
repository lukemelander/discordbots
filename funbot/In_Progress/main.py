import discord
import os
import nvdas
import env
import re
import random
from urllib.request import urlopen



client = discord.Client()



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    #if message.content.startswith('$hello'):
    #    await message.channel.send('Hello!')
    
    #if message.content.startswith('NVDA'):
    #    nvdas.nvdas +=1
    #    if nvdas.nvdas == 1:
    #        await message.channel.send('Stop it, Proph')

    #    if nvdas.nvdas == 2:
    #        await message.channel.send('Well, I tried. Good luck, guys.')
    #        nvdas.nvdas = 0
         
    spce = "SPCE"
    #if spce in message.content:
    #    await message.channel.send('Can\'t spell SPAC without SP....C... wait....')
    
    '''shut_up_bot = "Shut up funbot"
    if shut_up_bot in message.content:
        await message.channel.send('You shut up.')
        return
    '''    

    finance = "finance"
    if finance in message.content:
        await message.channel.send('I don\'t know finance. I just press buttons until RH turns green.')
    
    i_can_code = "I can code"    
    if i_can_code in message.content:
        await message.channel.send('Alas, PB cannot code.')        
        
    joke_list = ['ACTC', 'Proph rhymes with moth.... wait.... it doesn\'t? Oh well, NVDA is red today so take that.', 'Don\'t anger Hamie or he might move the market again.', 'In home country, wife leaves Tea.', 'According to Forbes, Proterra has thrown in the towel: "It doesn\'t matter that we\'re profitabl and well positioned, Hamie wouldn\'t hype us, so we don\'t really see a futurefor the company," says CEO Jack Allen.', 'PB\'s portfolio.', 'Roses are red, violets are blue, the US might split in 2.', 'Current interest rates.', 'The fed.', 'Pelosi.']
        
    funbot_joke = "Funbot joke"
    funbot_joke_2 = "Funbot, tell me a joke"
    if funbot_joke in message.content:
        await message.channel.send(random.choice(joke_list))
    
        
    '''
    nvda = "NVDA"
    if nvda in message.content:
        nvdas.nvdas +=1    
        if nvdas.nvdas == 1:
            await message.channel.send('Stop it, Proph')

        if nvdas.nvdas == 2:
            await message.channel.send('Not again ;(.')
            
        if nvdas.nvdas == 3:
            await message.channel.send('Have you ever heard of AMD? I hear they make pretty good graphics processors.')            

        if nvdas.nvdas == 4:
            await message.channel.send('Well, I tried. Good luck, guys.')
            nvdas.nvdas = 0
 
         
    pins = "PINS"
    if pins in message.content:
        nvdas.pins +=1    
        if nvdas.pins == 1:
            await message.channel.send('Stop it, Kagami.')        
        
        if nvdas.pins == 2:
            await message.channel.send('Can\'t spell PENIS without PINS.... slightly rearranged. BUT STILL!')
            
    women = "women"
    women_2 = "Women"
    if women in message.content:
        await message.channel.send('Long on women')               
    if women_2 in message.content:
        await message.channel.send('Long on women')              
    '''        
    url = "https://www.fun.com"
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode('utf-8')
    open_url = "F news"    
    if open_url in message.content:
        try:
            await message.channel.send(html) 
        except:
            exit()
client.run(env.TOKEN)
