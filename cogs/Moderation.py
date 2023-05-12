import discord
from discord.ext import commands
import predicates

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @predicates.has_perms_or_owner(administrator=True)
    @commands.command(name="clear")
    async def _clear(self, ctx, *, msg='1'):
        try:
            num_msgs = int(msg)
            if 0 < num_msgs <= 20:
                msgs = await ctx.channel.history(limit=num_msgs+1).flatten()
                await ctx.channel.delete_messages(msgs)
        except Exception as e:
            await ctx.send(f"Something went wrong")
            print(f"Clear exception: {e}")

    @predicates.has_perms_or_owner(administrator=True)
    @commands.command(name="cnick")
    async def _cnick(self, ctx, *, nick):
        ch = ctx.author.voice.channel
        if ch:
            await ch.edit(name=nick)

    @commands.is_owner()
    @commands.command(name="roles")
    async def _roles(self, ctx):
        roles = await ctx.guild.fetch_roles()
        rolestr = map(lambda x: f"{x.position}: {x.name}", roles)
        ch = await ctx.message.author.create_dm()
        await ch.send(sorted(rolestr))


async def setup(bot):
    await bot.add_cog(Moderation(bot))