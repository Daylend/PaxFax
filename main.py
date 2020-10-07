import discord
import logging
import random
import asyncio
from discord.ext import commands

master = "Daylend#0001"
masterid = 113156025984520192
guildid = 688826072187404290
blab_channelid = 689766528224460820
names = ["Daylend", "everyone", "nobody", "Brizz", "Nemo", "Snu", "Jay", "Panda", "Golddog", "Raiyun", "Spacefrog",
         "Zeropa", "Caldra", "Jael", "Seki", "Zen"]
cogs = ["Fun", "Owner", "Information", "Moderation", "Apocalypse"]
angrystuff_file = "paxfax_toxic.txt"
blabs_file = "paxfax.txt"
suggestion_file = "paxfax_suggestions.txt"
key_file = "key.txt"
prefix = '.'

class PaxFax(commands.AutoShardedBot):
    blabs = []
    angrystuff = []
    names = []
    slowmode = True
    debug = False
    attendance_channelid = 0

    def __init__(self):
        super().__init__(command_prefix=prefix, owner_id=masterid, reconnect=True, case_insensitive=True)

        self.embed_color = 0x0099FF

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        await self.load_cogs()
        await self.load_blabs()
        await self.load_angrystuff()

        self.blabtask = self.loop.create_task(self.blab_task())
        self.presencetask = self.loop.create_task(self.presence_task())


    async def blab_task(self):
        while True:
            delay = 0
            if self.slowmode:
                delay = random.randrange(3600*15,3600*24)
            else:
                delay = random.randrange(10*60,30*60)
            print(f"Waiting {delay} before next blab")
            await asyncio.sleep(delay)
            await self.blab()

    async def presence_task(self):
        while True:
            game = discord.Game(name='Yelling at {}'.format(self.names[random.randrange(len(self.names))]))
            await self.change_presence(activity=game)
            await asyncio.sleep(3600)

    async def on_message(self, message):
        if message.author == client.user:
            return

        if str(client.user) in message.content or str(client.user.id) in message.content:
            # Roll to see if we're saying an angry response
            if random.randrange(0,10) == 0:
                await message.channel.send('{} {}'.format(message.author.mention, self.blabs[random.randrange(len(self.blabs))]))
            else:
                await message.channel.send('{} {}'.format(message.author.mention, self.angrystuff[random.randrange(len(self.angrystuff))]))

        #print('Guild: {0.guild} Channel: {0.channel} From {0.author}: {0.content}'.format(message))
        await self.process_commands(message)

    async def blab(self):
        channel = await client.fetch_channel(blab_channelid)

        # Make sure the bot doesn't fill up chat
        if not client.user.id == channel.last_message_id:
            blab = self.blabs[random.randrange(len(self.blabs))]
            await channel.send(blab)
            print(f"Blabbed: {blab}")

    async def load_blabs(self):
        with open(blabs_file, encoding="utf-8") as f:
            self.blabs = f.read().splitlines()

    async def load_angrystuff(self):
        with open(angrystuff_file, encoding="utf-8") as f:
            self.angrystuff = f.read().splitlines()

    async def add_blab(self, message):
        with open(blabs_file, "a", encoding="utf-8") as f:
            f.write("\n" + message)

    async def add_angrystuff(self, message):
        with open(angrystuff_file, "a", encoding="utf-8") as f:
            f.write("\n" + message)

    async def add_suggestion(self, message):
        with open(suggestion_file, "a", encoding="utf-8") as f:
            f.write("\n" + message)

    async def load_cogs(self):
        try:
            for cog in cogs:
                self.load_extension(f"cogs.{cog}")
                print(f"Loaded cogs.{cog}")
        except Exception as e:
            print(f"Could not load extension {e}")

    async def reload_cogs(self):
        try:
            for cog in cogs:
                self.reload_extension(f"cogs.{cog}")
                print(f"Reloaded cogs.{cog}")
        except Exception as e:
            print(f"Could not load extension {e}")

def get_key():
    with open(key_file) as f:
        return f.readline()

if __name__ == '__main__':
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

    client = PaxFax()

    client.names = names
    client.run(get_key())