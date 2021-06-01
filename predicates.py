from discord.ext.commands import MissingPermissions, is_owner, has_permissions
from discord.ext import commands

# Checks if message came from apocalypse guild
def is_in_apocalypse():
    async def predicate(ctx):
        return ctx.guild and ctx.guild.id == 688826072187404290

    return commands.check(predicate)

# Makes exceptions for owner of bot
def has_perms_or_owner(**perms):
    async def predicate(ctx):
        return is_owner() or has_permissions(**perms)

    return commands.check(predicate)