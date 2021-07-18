import discord
from discord.ext import commands
import aiohttp
import random

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

    @commands.command(name='avatar')
    async def _avatar(self, ctx, member: discord.Member):
        embed = discord.Embed(
            color=self.bot.embed_color,
            title="→ Avatar"
        )
        embed.set_image(url=member.avatar_url_as(size=1024, format=None, static_format="png"))

        await ctx.send(embed=embed)

    @commands.command(name='suggest')
    async def _suggest(self, ctx, *, message):
        await self.bot.add_suggestion(message)
        await ctx.send("Your suggestion has been added to the suggestion box! Thank you")

    @commands.command()
    async def joke(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://official-joke-api.appspot.com/jokes/general/random') as r:
                res = await r.json()
                embed = discord.Embed(
                    color=self.bot.embed_color,
                    title="→ Random Joke!",
                    description=f"• Question: {res[0]['setup']}"
                                f"\n• Joke: {res[0]['punchline']}"
                )
                await ctx.send(embed=embed)

    @commands.command()
    async def coinflip(self, ctx):
        choices = ("Heads!", "Tails!")
        coin = random.choice(choices)
        embed = discord.Embed(
            color=self.bot.embed_color,
            title="→ Coinflip Command",
            description=f"• {coin}"
        )

        await ctx.send(embed=embed)

    @commands.command(name="8ball")
    async def _8ball(self, ctx, *, question, ):
        responses = ["It is certain.",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes - definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful."]
        embed = discord.Embed(
            color=self.bot.embed_color,
            title="→ 8Ball Command"
        )
        embed.add_field(name="• Question :grey_question: ", inline=False, value=f"{question}")
        embed.add_field(name="• Answer :8ball: ", inline=False, value=f"{random.choice(responses)}")

        await ctx.send(embed=embed)

    @_8ball.error
    async def _8ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                color=self.bot.embed_color
            )
            embed.add_field(name="→ Invalid Argument!",
                            value="• Please put in a valid option! Example: `l!8ball <question>`")
            await ctx.send(embed=embed)

    @commands.command(name="reroll")
    async def _reroll(self, ctx):
        classes = ["Berserker",
                   "Archer",
                   "Sorcerer",
                   "Tamer",
                   "Valkyrie",
                   "Warrior",
                   "Wizard",
                   "Witch",
                   "Musa",
                   "Maewha",
                   "Ninja",
                   "Kunoichi",
                   "Dark Knight",
                   "Striker",
                   "Mystic",
                   "Lahn",
                   "Ranger",
                   "Shai",
                   "Guardian",
                   "Hashashin",
                   "Nova",
                   "Sage",
                   "Corsair"]
        message = f"Congratulations, you are now a {random.choice(classes)}."
        await ctx.send(message=message)

def setup(bot):
    bot.add_cog(Fun(bot))