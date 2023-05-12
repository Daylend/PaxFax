import discord
from discord.ext import commands

class Information(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='about')
    async def _about(self, ctx):
        await ctx.send(f"Made by {await self.bot.fetch_user(self.bot.owner_id)}, send me a pm for any issues/suggestions.")

async def setup(bot):
    await bot.add_cog(Information(bot))