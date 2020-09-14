import discord
from discord.ext import commands

class Apocalypse(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    normalvc = 689760834955509764
    prepostvc = 688923192588632128
    offensevc = 688826072191598615
    flexvc = 688922427006255117
    testvc1 = 689760834955509764
    testvc2 = 691906650289864734
    flex_roleid = 712302975821021194

    async def move_category_to_vc(self, vcc, vc, exclude_names=None):
        # Move everyone in normal voice category to prepost
        if exclude_names is None:
            exclude_names = ["afk"]
        for v in vcc.voice_channels:
            # Don't move people from channels that contain strings found in exclude_names
            if not any(v.name.lower() in name.lower() for name in exclude_names):
                for member in v.members:
                    await member.move_to(vc)

    @commands.has_permissions(administrator=True)
    @commands.command(name="move")
    async def _move(self, ctx, *, msg):
        # Moves everyone from normal voice channels to pre/post
        if msg == "prewar":
            normalvc = await self.bot.fetch_channel(self.normalvc)
            prepostvc = await self.bot.fetch_channel(self.prepostvc)
            normalvcc = normalvc.category

            await self.move_category_to_vc(normalvcc, prepostvc)
        # Moves everyone from pre/post to offense/flex depending on role
        elif msg == "war":
            prepostvc = await self.bot.fetch_channel(self.prepostvc)
            offensevc = await self.bot.fetch_channel(self.offensevc)
            flexvc = await self.bot.fetch_channel(self.flexvc)
            flexrole = prepostvc.guild.get_role(self.flex_roleid)

            for member in prepostvc.members:
                if flexrole in member.roles:
                    await member.move_to(flexvc)
                else:
                    await member.move_to(offensevc)

        # Moves everyone from other war voice channels to pre/post
        elif msg == "postwar":
            prepostvc = await self.bot.fetch_channel(self.prepostvc)
            warvcc = prepostvc.category

            await self.move_category_to_vc(warvcc, prepostvc, ["Pre/Post War/RBF"])
        # Moves everyone from war voice channels to normal vc
        elif msg == "endwar":
            prepostvc = await self.bot.fetch_channel(self.prepostvc)
            warvcc = prepostvc.category
            normalvc = await self.bot.fetch_channel(self.normalvc)

            await self.move_category_to_vc(warvcc, normalvc)
        """elif msg == "clone":
            mem = ctx.author
            vc = mem.voice.channel

            if vc is not None:
                invites = await vc.invites()
                if len(invites)<1:
                    vc2 = await vc.clone(reason="Moving people to new channel")
                    for member in vc.members:
                        await member.move_to(vc2)
                else:
                    await ctx.send("Can't clone current channel as it has invites")"""

    attendance_channelid = 704239533914324992
    attendance_guildid = 688826072187404290
    member_roleid = 688944180298514440
    yes_emote = "CheckmarkNeon"
    maybe_emote = "Neon_Maybe"
    no_emote = "XNeon"
    emotedict = {yes_emote: "Yes'd Up", maybe_emote: "Maybe Going", no_emote: "Not Coming"}

    # Get all members with a specific roleid
    async def get_members_with_role(self, ctx, roleid):
        members = []
        role = ctx.guild.get_role(roleid)
        for member in ctx.guild.members:
            if role in member.roles:
                members.append(member)
        return members

    async def find_members_with_reacts(self, msgs, reactemotes):
        reactusers = []
        for msg in msgs:
            for reaction in msg.reactions:
                # Look for emotes we actually care about
                if reaction.emoji.name in reactemotes:
                    users = await reaction.users().flatten()
                    # Add them to the nice list
                    for user in users:
                        if not user in reactusers:
                            reactusers.append(user)
        return reactusers

    async def find_message_with_attachment(self, msgs, filename):
        for msg in msgs:
            for attachment in msg.attachments:
                if filename.lower() in attachment.filename.lower():
                    return msg
        return None

    async def print_users(self, ctx, embed, users):
        # Print all members left over who haven't reacted
        for user in users:
            # If there's more than 25 fields we need to send another embed
            if len(embed.fields) >= 25:
                await ctx.send(embed=embed)
                embed = discord.Embed(
                    color=self.bot.embed_color
                )
            if user.nick is not None:
                embed.add_field(name=user.nick, value=str(user), inline=True)
            else:
                embed.add_field(name=str(user), value="None", inline=True)

        if len(embed.fields) > 0:
            await ctx.send(embed=embed)

    async def get_url_from_emoji_name(self, msgs, emojiname):
        for msg in msgs:
            for reaction in msg.reactions:
                if reaction.emoji.name in emojiname:
                    return reaction.emoji.url
        return None

    @commands.command(name='remind')
    async def _remind(self, ctx):
        # We only want this to run if we're in the guild discord
        if ctx.guild.id != self.attendance_guildid:
            return

        # Get a list of all members with the "member" role
        members = await self.get_members_with_role(ctx, self.member_roleid)

        # Get all msgs in attendance ch
        ch = await self.bot.fetch_channel(self.attendance_channelid)
        msgs = await ch.history(limit=100).flatten()
        reactemotes = [self.yes_emote, self.maybe_emote, self.no_emote]
        reactusers = await self.find_members_with_reacts(msgs, reactemotes)

        # Remove members that have already reacted
        for user in reactusers:
            if user in members:
                members.remove(user)

        embed = discord.Embed(
            color=self.bot.embed_color,
            title=f"Attendance Report ({len(members)})",
            description=f"Current list of members who have not reacted to attendance this week."
                        f" {len(members)} have not signed up."
        )

        await self.print_users(ctx, embed, members)

    @commands.command(name='attendance')
    async def _attendance(self, ctx, *, msg):
        # We only want this to run if we're in the guild discord
        if ctx.guild.id != self.attendance_guildid:
            return

        async with ctx.channel.typing():
            ch = await self.bot.fetch_channel(self.attendance_channelid)
            msgs = await ch.history(limit=100).flatten()
            reactemotes = [self.yes_emote, self.maybe_emote, self.no_emote]
            reactmsg = await self.find_message_with_attachment(msgs, msg)

            embed = discord.Embed(
                color=self.bot.embed_color,
                title=f"Attendance Report ({msg})",
                description=f"Current list of members who have reacted for {msg}"
            )
            await ctx.send(embed=embed)

            for react in reactemotes:
                url = await self.get_url_from_emoji_name(msgs, react)
                reactusers = await self.find_members_with_reacts([reactmsg], [react])
                reactusers.sort(key=lambda x: x.display_name)

                embed = discord.Embed(
                        color=self.bot.embed_color,
                        title=f"{self.emotedict[react]} ({len(reactusers)})",
                )
                embed.set_thumbnail(url=url)
                embed.url=reactmsg.jump_url
                await self.print_users(ctx, embed, reactusers)

    @commands.has_permissions(administrator=True)
    @commands.command(name='notify')
    async def _notify(self, ctx):
        # We only want this to run if we're in the guild discord
        if ctx.guild.id != self.attendance_guildid:
            return

        # Get a list of all members with the "member" role
        members = await self.get_members_with_role(ctx, self.member_roleid)

        # Get all msgs in attendance ch
        ch = await self.bot.fetch_channel(self.attendance_channelid)
        msgs = await ch.history(limit=100).flatten()
        reactemotes = [self.yes_emote, self.maybe_emote, self.no_emote]
        reactusers = await self.find_members_with_reacts(msgs, reactemotes)

        # Remove members that have already reacted
        for user in reactusers:
            if user in members:
                members.remove(user)

        embed = discord.Embed(
            color=self.bot.embed_color,
            title=f"Attendance Report ({len(members)})",
            description=f"Current list of members who have not reacted to attendance this week."
                        f" {len(members)} have not signed up."
        )

        #await self.print_users(ctx, embed, members)
        #await ctx.send(f"Notified {len(members)} members.")

        printmsg = "Fake mentions for testing: "
        for member in members:
            printmsg += f"{member.display_name} "
        printmsg += f"\n\nThis is your reminder to react to attendance for the week." \
                    f"  As of right now, **{len(members)}** have not reacted this week. " \
                    f"Remember, this may not seem like it's very important, " \
                    f"but we use it to make sure we're on the right size nodes, " \
                    f"so it's information we really need. Thank you!"
        await ctx.send(printmsg)

def setup(bot):
    bot.add_cog(Apocalypse(bot))