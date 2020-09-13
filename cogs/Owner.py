from discord.ext import commands

class Owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(aliases=["slowmode"])
    async def _slowmode(self, ctx):
        self.bot.slowmode = not self.bot.slowmode
        self.bot.blabtask.cancel()
        self.bot.blabtask = self.bot.loop.create_task(self.bot.blab_task())
        await ctx.send(f"Slowmode {'ON' if self.bot.slowmode else 'OFF'}")

    @commands.is_owner()
    @commands.command(aliases=["reload"])
    async def _reload(self, ctx):
        await self.bot.reload_cogs()
        await ctx.send(f"Cogs reloaded")

def setup(bot):
    bot.add_cog(Owner(bot))