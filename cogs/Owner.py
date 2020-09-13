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
        await self.bot.load_blabs()
        await self.bot.load_angrystuff()
        await ctx.send(f"Reloaded")

    @commands.is_owner()
    @commands.command(aliases=["add"])
    async def _add(self, ctx, arg1, *, arg2):
        if arg1 == "blab":
            await self.bot.add_blab(arg2)
            await self.bot.load_blabs()
        elif arg1 == "angry":
            await self.bot.add_angrystuff(arg2)
            await self.bot.load_angrystuff()
        else:
            await ctx.send("Something went wrong")
        await ctx.send(f"Added \"{arg2}\" to {arg1}")

    @commands.is_owner()
    @commands.command(aliases=["clear"])
    async def _clear(self, ctx, *, msg='1'):
        try:
            num_msgs = int(msg)
            if 0 < num_msgs <= 20:
                msgs = await ctx.channel.history(limit=num_msgs).flatten()
                await ctx.channel.delete_messages(msgs)
        except Exception as e:
            await ctx.send(f"Something went wrong")
            print(f"Clear exception: {e}")

    @commands.is_owner()
    @commands.command(aliases=["echo"])
    async def _echo(self, ctx, *, msg):
        await ctx.message.delete()
        await ctx.send(msg)



def setup(bot):
    bot.add_cog(Owner(bot))