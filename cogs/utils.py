import discord
from discord.ext import commands

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def load(self, ctx, extension):
        await self.bot.load_extension(f'cogs.{extension}')
        await ctx.reply(f'{extension} loaded')

    @commands.command()
    async def unload(self, ctx, extension):
        await self.bot.unload_extension(f'cogs.{extension}')
        await ctx.reply(f'{extension} unloaded')
    
    @commands.command()
    async def updateExt(self, ctx, extension):
        try:
            await self.bot.unload_extension(f'cogs.{extension}')
        except:
            await self.bot.load_extension(f'cogs.{extension}')
        else:
            await self.bot.load_extension(f'cogs.{extension}')

async def setup(bot):
    await bot.add_cog(Utils(bot))