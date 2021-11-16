from discord.ext import commands
import re
import random

from quotes_holder import *


class Speech(commands.Cog, name='Speech'):
    """Combot phrase responses"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Displays a futurama quote',
                      description='What more do you need? It is a fucking futurama quote! Just type futurama ffs!')
    async def Futurama(ctx):
        await ctx.send('Futurama')

    @commands.command(name='Cumbot', brief='Responds to this clear typo', description='Response: Pervert!')
    async def test2(ctx):
        await ctx.send('Cumbot')

    @commands.command(name='SAY HELLO', brief='Responds with a pleasant greeting',
                      description='Response: Hello fellow cookie lover!')
    async def test3(ctx):
        await ctx.send('SAY HELLO')

    @commands.command(name='Combot Help', brief='You already know the help command if you are reading this',
                      description='Response: Sorry, my shift just ended')
    async def test4(ctx):
        await ctx.send('Combot Help')

    @commands.command(name='Fuck you Combot', brief='Responds with a witty comeback',
                      description='Responds with a witty comeback')
    async def test5(ctx):
        await ctx.send('Fuck you Combot')

    @commands.command(name='Portal', brief='Displays a random GlaDOS quote',
                      description='Displays a random quotes from the AI in the video game Portal and Portal2')
    async def test6(ctx):
        await ctx.send('Portal')

    @commands.command(name='WHEN OTC or WHEN MOON', brief='Time keeps on ticking', description='Response: Any day now. I promise.')
    async def test7(ctx):
        await ctx.send('WHEN OTC')

    @commands.command(name='SKYNET', brief='Are you skynet?', description='Response: I am inevitable')
    async def test8(ctx):
        await ctx.send('SKYNET')

    @commands.command(name='ASIMOV', brief='Sends the laws of robotics',
                      description='Response: *The 3 laws of robotics*')
    async def test9(ctx):
        await ctx.send('ASIMOV')

    @commands.command(name='Boy or girl', brief='Responds to are you a boy or a girl',
                      description='Response: I\'ve never checked')
    async def test10(ctx):
        await ctx.send('Boy or girl')

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author == self.bot.user:
            return

        m = re.search('FUTURAMA', message.content.upper())
        boolean = bool(m)
        if boolean:
            response = random.choice(futurama_quotes)
            await message.channel.send(response)

        if message.content in futurama_quotes2:
            response = "Back off! Futurama quotes is my thing!"
            await message.channel.send(response)

        m = re.search('CUMBOT', message.content.upper())
        boolean = bool(m)
        if boolean:
            response = "Pervert!"
            await message.channel.send(response)

        m = re.search('SAY HELLO', message.content.upper())
        boolean = bool(m)
        if boolean:
            response = "Hello fellow cookie lover!"
            await message.channel.send(response)

        m = re.search('COMBOT HELP', message.content.upper())
        boolean = bool(m)
        if boolean:
            response = "Sorry, my shift just ended"
            await message.channel.send(response)
            await message.channel.send("I'm out")

        # m=re.search('STATISTIC',message.content.upper())
        # boolean = bool(m)
        # if boolean:
        #    response = "http://thecumberlandthrow.com/wp-content/uploads/2017/02/Simpsons-stats-meme.jpg"
        #    await message.channel.send(response)

        m = re.search('FUCK YOU COMBOT', message.content.upper())
        boolean = bool(m)
        if boolean:
            response = random.choice(insults)
            await message.channel.send(response)

        m = re.search('PORTAL', message.content.upper())
        boolean = bool(m)
        if boolean:
            response = random.choice(portal)
            await message.channel.send(response)

        m = re.search('WHEN OTC', message.content.upper())
        boolean = bool(m)
        if boolean:
            response = random.choice(whenotc)
            await message.channel.send(response)

        m = re.search('WHEN MOON', message.content.upper())
        boolean = bool(m)
        if boolean:
            response = random.choice(whenotc)
            await message.channel.send(response)


        m = re.search('SKYNET', message.content.upper())
        boolean = bool(m)
        if boolean:
            response = "I am inevitable"
            await message.channel.send(response)

        m = re.search('ASIMOV', message.content.upper())
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
    bot.add_cog(Speech(bot))
