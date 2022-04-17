import asyncio
from io import BytesIO
import json
import discord
from discord.ext import commands
from discord.ext.commands import is_owner, has_permissions
from discord.utils import get
from gtts import gTTS
from os import listdir
from os.path import isfile, join

class Voice(commands.Cog):

    fxpath = "./sfx/"
    ext = ".mp3"

    def __init__(self, bot):
        self.bot = bot
        self.accent = {}
        self.load_accents()

    def can_speak():
        async def predicate(ctx):
            mute_role = ctx.guild.get_role(811148263935180811)
            has_mute = mute_role in ctx.author.roles
            isowner = False
            hasperms = False
            try:
                isowner = await is_owner().predicate(ctx)
            except:
                pass
            
            try:
                hasperms = await has_permissions(administrator=True).predicate(ctx)
            except:
                pass
            return has_mute or isowner or hasperms
        return commands.check(predicate)

    def is_connected(self, ctx):
        voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
        return voice_client and voice_client.is_connected()

    def load_accents(self):
        try:
            with open("accent.json", "r") as f:
                self.accent = json.loads(f.read())
        except:
            self.accent = {}

    def save_accents(self):
        try:
            with open("accent.json", "w") as f:
                f.write(json.dumps(self.accent))
        except:
            pass

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
        if (msg == "?"):
            files = [f for f in listdir(self.fxpath) if isfile(join(self.fxpath, f))]
            await ctx.send(str(files))
            return
        if not ctx.voice_client:
            await self._join(ctx)
        if ctx.voice_client:
            ffpath = "C:\\Program Files (x86)\\FFmpeg for Audacity\\ffmpeg.exe"

            path = self.fxpath + msg + self.ext
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(path), volume=0.75)
            # Local version
            # source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(path, executable=ffpath), volume=0.75)
            ctx.voice_client.play(source)

    @commands.command(name="say")
    @can_speak()
    async def _say(self, ctx, *, msg):
        if not ctx.voice_client:
            await self._join(ctx)
        if ctx.voice_client:
            accent = 'ca'
            if ctx.message.author.id in self.accent:
                accent = self.accent[ctx.message.author.id]

            tts = gTTS(msg, lang='en', tld=accent)
            path = self.fxpath + 'tts' + self.ext
            tts.save(path)
            ffpath = "C:\\Program Files (x86)\\FFmpeg for Audacity\\ffmpeg.exe"
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(path), volume=0.75)
            # Local version
            # source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(path, executable=ffpath), volume=0.75)
            ctx.voice_client.play(source)

    @commands.command(name="accent")
    @can_speak()
    async def _accent(self, ctx, *, msg):
        accents = {
                'aus': 'com.au',
                'uk': 'co.uk',
                'us': 'ca',
                'india': 'co.in'
            }
        
        if msg in accents: 
            self.accent[ctx.message.author.id] = accents[msg]
            await ctx.send(f'Your accent has been set to "{msg}"')
            self.save_accents()
        else: await ctx.send(accents.keys())

def setup(bot):
    bot.add_cog(Voice(bot))
