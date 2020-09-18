import discord
from discord.ext import commands

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
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

def setup(bot):
    bot.add_cog(Moderation(bot))