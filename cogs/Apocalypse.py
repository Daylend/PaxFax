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
    role_prefix = "attendance_"
    announcement_chid = 756330674927173693
    attendance_channelid = 704239533914324992
    apocalypse_guildid = 688826072187404290
    member_roleid = 688944180298514440
    yes_emote = "CheckmarkNeon"
    maybe_emote = "Neon_Maybe"
    no_emote = "XNeon"
    emotedict = {yes_emote: "Yes'd Up", maybe_emote: "Maybe Going", no_emote: "Not Coming"}

    # Can't use self without runtime error?
    def is_in_apocalypse():
        async def predicate(ctx):
            return ctx.guild and ctx.guild.id == 688826072187404290
        return commands.check(predicate)

    async def move_category_to_vc(self, vcc, vc, exclude_names=None):
        # Move everyone in normal voice category to prepost
        if exclude_names is None:
            exclude_names = ["afk"]
        for v in vcc.voice_channels:
            # Don't move people from channels that contain strings found in exclude_names
            if not any(v.name.lower() in name.lower() for name in exclude_names):
                for member in v.members:
                    await member.move_to(vc)

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

    async def get_role_from_guild(self, guild, rolename):
        # Check to see if role exists
        for role in guild.roles:
            if role.name == rolename:
                # Don't return admin roles because I don't want to break something
                if role.permissions.administrator is not True:
                    return role
        return None

    @is_in_apocalypse()
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

    @is_in_apocalypse()
    @commands.command(name='remind')
    async def _remind(self, ctx):
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

    @is_in_apocalypse()
    @commands.command(name='attendance')
    async def _attendance(self, ctx, *, msg):
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


    @is_in_apocalypse()
    @commands.has_permissions(administrator=True)
    @commands.command(name='announce')
    async def _announce(self, ctx, day, *, msg):
        tempmsg = await ctx.send("Working... Please wait around 60 seconds.")
        day = day.lower()

        announcement_ch = await self.bot.fetch_channel(self.announcement_chid)

        # Delete old attendance roles
        for role in ctx.guild.roles:
            if role.name.startswith(self.role_prefix):
                # Make sure we're not deleting something important
                if role.permissions.administrator is not True:
                    await role.delete(reason="New announcement")

        newrole = await ctx.guild.create_role(name=self.role_prefix + day, reason="New announcement")

        ch = await self.bot.fetch_channel(self.attendance_channelid)
        msgs = await ch.history(limit=100).flatten()
        reactemotes = [self.yes_emote, self.maybe_emote]
        reactmsg = await self.find_message_with_attachment(msgs, day)
        if reactmsg is not None:
            reactusers = await self.find_members_with_reacts([reactmsg], reactemotes)

            for member in reactusers:
                if type(member) is discord.Member:
                    await member.add_roles(newrole, reason="New announcement")

            # There shouldn't be more than 20 msgs. Just in case. :)
            await announcement_ch.purge(limit=20)
            await announcement_ch.set_permissions(newrole, read_messages=True, read_message_history=True)
            await announcement_ch.send(f"{newrole.mention} {msg}")
            #await announcement_ch.send(f"TEST: {newrole.name} {msg}")
        await tempmsg.delete()

    @_announce.error
    async def _announce_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Syntax error in command. Syntax: ```.announce <day> <message>```\n"
                           "Example: ```.announce tuesday Hey guys war is on val1 today```")
        elif isinstance(error, commands.CommandOnCooldown):
            pass
        else:
            await ctx.send("Something went wrong. Unable to announce. :(")

    @is_in_apocalypse()
    @commands.has_permissions(administrator=True)
    @commands.command(name='notify')
    async def _notify(self, ctx):
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

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = await self.bot.fetch_channel(payload.channel_id)
        user = await channel.guild.fetch_member(payload.user_id)
        message = await channel.fetch_message(payload.message_id)
        # Is it this bot's message and is the user reacting not the bot
        # reaction.message.author == reaction.message.guild.me and
        if user is not message.guild.me:
            going_reactions = [self.yes_emote, self.maybe_emote]
            # If it's a reaction to attendance
            if message.channel.id == self.attendance_channelid:
                # If the message has an attachment
                if len(message.attachments) == 1:
                    # If it's an "attending" reaction
                    if payload.emoji.name in going_reactions:
                        # Get attachment name to use as role name
                        name = message.attachments[0].filename.split('.')[0].lower()
                        role = await self.get_role_from_guild(message.guild, self.role_prefix+name)
                        if role is not None:
                            await user.add_roles(role, reason="Announcement role")
                        else:
                            newrole = await message.guild.create_role(name=self.role_prefix+name,
                                                                               reason="New announcement")
                            await user.add_roles(newrole, reason="Announcement role")
                            announcement_ch = await self.bot.fetch_channel(self.announcement_chid)
                            await announcement_ch.set_permissions(newrole, read_messages=True, read_message_history=True)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        channel = await self.bot.fetch_channel(payload.channel_id)
        user = await channel.guild.fetch_member(payload.user_id)
        message = await channel.fetch_message(payload.message_id)
        # Is it this bot's message and is the user reacting not the bot
        # reaction.message.author == reaction.message.guild.me and
        if user is not message.guild.me:
            going_reactions = [self.yes_emote, self.maybe_emote]
            # If it's a reaction to attendance
            if message.channel.id == self.attendance_channelid:
                # If the message has an attachment
                if len(message.attachments) == 1:
                    # If it's an "attending" reaction
                    if payload.emoji.name in going_reactions:
                        name = message.attachments[0].filename.split('.')[0].lower()
                        role = await self.get_role_from_guild(message.guild, self.role_prefix+name)
                        if role is not None:
                            await user.remove_roles(role, reason="Removed reaction from attendance")

def setup(bot):
    bot.add_cog(Apocalypse(bot))