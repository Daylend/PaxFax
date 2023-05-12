from discord import Permissions
from discord.ext import commands

# Checks if message came from apocalypse guild
def is_in_apocalypse():
    async def predicate(ctx):
        return ctx.guild and ctx.guild.id == 688826072187404290

    return commands.check(predicate)

# Makes exceptions for owner of bot and specified permissions
def has_perms_or_owner(**perms):
    async def predicate(ctx):
        # Check if the author is the owner of the bot
        owner = await ctx.bot.is_owner(ctx.author)

        # Check if the author has the specified permissions
        has_perms = ctx.author.guild_permissions >= Permissions(**perms)

        return owner or has_perms

    return commands.check(predicate)