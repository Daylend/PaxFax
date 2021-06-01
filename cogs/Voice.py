import asyncio
from io import BytesIO

import discord
from discord.ext import commands
from discord.ext.commands import is_owner, has_permissions
from discord.utils import get
from gtts import gTTS

class Voice(commands.Cog):

    fxpath = "./sfx/"
    ext = ".mp3"

    def __init__(self, bot):
        self.bot = bot

    def can_speak():
        async def predicate(ctx):
            mute_role = ctx.guild.get_role(811148263935180811)
            has_mute = mute_role in ctx.author.roles
            has_perms = is_owner() or has_permissions(administrator=True)
            return has_mute or has_perms
        return commands.check(predicate)

    def is_connected(self, ctx):
        voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
        return voice_client and voice_client.is_connected()

    @commands.command(name="join")
    @commands.is_owner()
    async def _join(self, ctx):
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(ctx.author.voice.channel)
        vc = await ctx.author.voice.channel.connect()
        vc.stop()

    @commands.command(name="leave")
    @can_speak()
    async def _leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()

    @commands.command(name="sb")
    @can_speak()
    async def _sb(self, ctx, *, msg):
        if not ctx.voice_client:
            await self._join(ctx)
        if ctx.voice_client:
            ffpath = "C:\\Program Files (x86)\\FFmpeg for Audacity\\ffmpeg.exe"

            path = self.fxpath + msg + self.ext
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(path, executable=ffpath), volume=0.75)
            ctx.voice_client.play(source)

    @commands.command(name="say")
    @can_speak()
    async def _say(self, ctx, *, msg):
        if not ctx.voice_client:
            await self._join(ctx)
        if ctx.voice_client:
            tts = gTTS(msg, lang='en', tld='ca')
            path = self.fxpath + 'tts' + self.ext
            tts.save(path)
            ffpath = "C:\\Program Files (x86)\\FFmpeg for Audacity\\ffmpeg.exe"
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(path, executable=ffpath), volume=0.75)
            ctx.voice_client.play(source)

def setup(bot):
    bot.add_cog(Voice(bot))