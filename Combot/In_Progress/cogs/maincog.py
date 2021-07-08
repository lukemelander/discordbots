from discord.ext import commands
import re
import random

from quotes_holder import *

class MainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.Cog.listener()
    async def on_message(self,message):

        if message.author == self.bot.user:
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


def setup(bot):
    bot.add_cog(MainCog(bot))