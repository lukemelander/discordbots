import discord
from discord.ext import commands
import requests


class Animals(commands.Cog, name='Animals'):
    """Random animal pictures!"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='cat', brief='Shows a random cat picture', description='Fetches a random cat picture from the internet!')
    async def cat(self, ctx):
        try:
            response = requests.get('https://api.thecatapi.com/v1/images/search')
            data = response.json()
            cat_url = data[0]['url']
            
            embed = discord.Embed(title='🐱 Random Cat!', color=0xFFA500)
            embed.set_image(url=cat_url)
            await ctx.send(embed=embed)
        except:
            await ctx.send("Sorry, couldn't fetch a cat picture right now 😿")

    @commands.command(name='dog', brief='Shows a random dog picture', description='Fetches a random dog picture from the internet!')
    async def dog(self, ctx):
        try:
            response = requests.get('https://dog.ceo/api/breeds/image/random')
            data = response.json()
            dog_url = data['message']
            
            embed = discord.Embed(title='🐶 Random Dog!', color=0x8B4513)
            embed.set_image(url=dog_url)
            await ctx.send(embed=embed)
        except:
            await ctx.send("Sorry, couldn't fetch a dog picture right now 🐕")

    @commands.command(name='catfact', brief='Shows a random cat fact', description='Learn something new about cats!')
    async def catfact(self, ctx):
        try:
            response = requests.get('https://catfact.ninja/fact')
            data = response.json()
            fact = data['fact']
            
            embed = discord.Embed(title='🐱 Cat Fact!', description=fact, color=0xFFA500)
            await ctx.send(embed=embed)
        except:
            await ctx.send("Sorry, couldn't fetch a cat fact right now 😿")


async def setup(bot):
    await bot.add_cog(Animals(bot))
