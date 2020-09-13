import discord
from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    async def _ping(self, ctx):
        await ctx.send("Pong!")
        print("Pong!")

    @_ping.error
    async def _ping_error(self, ctx, error):
        await ctx.send("Something went wrong apparently idk")

    @commands.command(aliases=['avatar'])
    async def _avatar(self, ctx, member: discord.Member):
        embed = discord.Embed(
            color=self.bot.embed_color,
            title="→ Avatar"
        )
        embed.set_image(url=member.avatar_url_as(size=1024, format=None, static_format="png"))

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))