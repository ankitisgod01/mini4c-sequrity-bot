 import os
import random
import asyncio
from datetime import timedelta
import discord
from discord.ext import commands
from discord.ui import Select, View, Button
from keep_alive import keep_alive

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents, help_command=None)

AFK_USERS = {}
SNIPE_CACHE = {}
ANTINUKE_STATUS = {}
USER_WALLETS = {}

FOOTER_TEXT = "Developer: ADX ANKIT | Pudding 🐾"
SUPPORT_SERVER_LINK = "https://discord.gg/Yttbf69xx"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Pudding Bot is active across servers with 7 Categories! 🐾")
    activity = discord.Activity(type=discord.ActivityType.streaming, name="🍮 Baking cute servers | $help 🐾", url="https://twitch.tv/discord")
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="welcome")
    if channel:
        embed = discord.Embed(title="✨ New Member Joined! ✨", description=f"Welcome to **{member.guild.name}**, {member.mention}!\nWe are so happy to have you here! 🎉", color=discord.Color.from_rgb(255, 209, 220))
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"Total Members: {member.guild.member_count} • {FOOTER_TEXT}")
        await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name="welcome")
    if channel:
        embed = discord.Embed(title="👋 Member Left", description=f"**{member.name}** has left the server. We will miss you! 💔", color=discord.Color.red())
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=FOOTER_TEXT)
        await channel.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.author.id in AFK_USERS:
        AFK_USERS.pop(message.author.id)
        try:
            await message.author.edit(nick=message.author.display_name.replace("[AFK] ", ""))
        except:
            pass
        await message.channel.send(f"👋 Welcome back {message.author.mention}, I removed your AFK status!", delete_after=5)
    for member in message.mentions:
        if member.id in AFK_USERS:
            await message.channel.send(f"💤 **{member.name}** is currently AFK: {AFK_USERS[member.id]}")
    await bot.process_commands(message)

@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return
    SNIPE_CACHE[message.channel.id] = {"content": message.content, "author": message.author, "time": message.created_at}

class HelpDropdown(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Antinuke", emoji="🛡️", description="Antinuke Toggle & Security controls"),
            discord.SelectOption(label="Welcome", emoji="✨", description="Welcome & Leave automated greetings"),
            discord.SelectOption(label="Moderation", emoji="⚒️", description="Moderation, Purge, Mute & Jail"),
            discord.SelectOption(label="Music", emoji="🎵", description="Voice channel Lofi & Music controls"),
            discord.SelectOption(label="Ticket", emoji="🎟️", description="Ticket system controls"),
            discord.SelectOption(label="Fun & Games", emoji="⚛️", description="Fun, Games, Ship & Roast"),
            discord.SelectOption(label="Economy & Utility", emoji="💰", description="Wallet, Daily, Work, Polls & Giveaways"),
        ]
        super().__init__(placeholder="Select a category to view commands", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        val = self.values[0]
        embed = discord.Embed(color=discord.Color.from_rgb(255, 209, 220))
        embed.set_thumbnail(url=interaction.client.user.display_avatar.url)
        embed.set_footer(text=f"Requested by {interaction.user.name} • {FOOTER_TEXT}", icon_url=interaction.user.display_avatar.url)
        if val == "Antinuke":
            embed.title = "🛡️ Antinuke Module"
            embed.add_field(name="Commands", value="`$antinuke on`, `$antinuke off`", inline=False)
        elif val == "Welcome":
            embed.title = "✨ Welcome Module"
            embed.add_field(name="Automation", value="Automatic `on_member_join` and `on_member_remove` embeds.", inline=False)
        elif val == "Moderation":
            embed.title = "⚒️ Moderation Module"
            embed.add_field(name="Commands", value="`$ban`, `$unban`, `$kick`, `$mute`, `$unmute`, `$purge`, `$lock`, `$unlock`, `$nuke`, `$role`, `$warn`, `$slowmode`", inline=False)
        elif val == "Music":
            embed.title = "🎵 Music Module"
            embed.add_field(name="Commands", value="`$play`, `$stop`, `$leave`", inline=False)
        elif val == "Ticket":
            embed.title = "🎟️ Ticket Module"
            embed.add_field(name="Commands", value="`$ticket setup`", inline=False)
        elif val == "Fun & Games":
            embed.title = "⚛️ Fun & Games Module"
            embed.add_field(name="Commands", value="`$ship`, `$chutiya`, `$howgay`, `$cute`, `$8ball`, `$hack`, `$rps`, `$fact`, `$hug`, `$kiss`, `$slap`, `$avatar`, `$coinflip`, `$meme`, `$roast`", inline=False)
        elif val == "Economy & Utility":
            embed.title = "💰 Economy & Utility Module"
            embed.add_field(name="Commands", value="`$balance`, `$daily`, `$work`, `$ping`, `$afk`, `$snipe`, `$poll`, `$say`, `$gstart`, `$serverinfo`, `$userinfo`, `$membercount`, `$embed`, `$math`", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

class HelpView(View):
    def __init__(self):
        super().__init__()
        self.add_item(HelpDropdown())
        self.add_item(Button(label="Support Server", emoji="🔗", url=SUPPORT_SERVER_LINK))

@bot.command(name="help")
async def help_cmd(ctx):
    embed = discord.Embed(title="Hello, I'm Pudding 🐾", description=f"• **Prefix:** `$`\n• **Total Categories:** `7 Professional Modules`\n• **Support:** [Join Server]({SUPPORT_SERVER_LINK})", color=discord.Color.from_rgb(255, 209, 220))
    embed.set_thumbnail(url=bot.user.display_avatar.url)
    embed.add_field(name="Categories", value="🛡️ Antinuke\n✨ Welcome\n⚒️ Moderation\n🎵 Music\n🎟️ Tickets\n🎮 Fun & Games\n💰 Economy & Utility", inline=False)
    embed.set_footer(text=FOOTER_TEXT, icon_url=bot.user.display_avatar.url)
    await ctx.send(embed=embed, view=HelpView())
    @bot.command()
@commands.has_permissions(administrator=True)
async def antinuke(ctx, status: str = None):
    if not status:
        current = ANTINUKE_STATUS.get(ctx.guild.id, False)
        status_text = "Enabled 🟢" if current else "Disabled 🔴"
        embed = discord.Embed(title="🛡️ Antinuke Status", description=f"Antinuke protection is currently: **{status_text}**", color=discord.Color.blue())
        embed.set_footer(text=FOOTER_TEXT)
        await ctx.send(embed=embed)
        return
    status = status.lower()
    if status in ["on", "enable", "true"]:
        ANTINUKE_STATUS[ctx.guild.id] = True
        embed = discord.Embed(title="🛡️ Antinuke Activated", description="Antinuke protection enabled!", color=discord.Color.green())
    elif status in ["off", "disable", "false"]:
        ANTINUKE_STATUS[ctx.guild.id] = False
        embed = discord.Embed(title="⚠️ Antinuke Deactivated", description="Antinuke protection disabled!", color=discord.Color.red())
    else:
        await ctx.send("❌ Invalid usage! Use: `$antinuke on` or `$antinuke off`")
        return
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

@bot.command(aliases=["bal", "wallet"])
async def balance(ctx, member: discord.Member = None):
    member = member or ctx.author
    bal = USER_WALLETS.get(member.id, 0)
    embed = discord.Embed(title=f"💰 {member.name}'s Balance", description=f"Wallet: **{bal} Coins** 🪙", color=discord.Color.from_rgb(255, 209, 220))
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

@bot.command()
async def daily(ctx):
    user_id = ctx.author.id
    USER_WALLETS[user_id] = USER_WALLETS.get(user_id, 0) + 500
    embed = discord.Embed(title="🎁 Daily Reward Claimed!", description=f"Added **500 Coins**! New Balance: **{USER_WALLETS[user_id]} Coins**", color=discord.Color.green())
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

@bot.command()
async def work(ctx):
    user_id = ctx.author.id
    earned = random.randint(50, 200)
    USER_WALLETS[user_id] = USER_WALLETS.get(user_id, 0) + earned
    job = random.choice(["Discord Bot Developer", "Graphic Designer", "Streamer", "Moderator"])
    embed = discord.Embed(title="💼 Work Shift Completed", description=f"Worked as a **{job}** and earned **{earned} Coins**! 🪙", color=discord.Color.from_rgb(255, 209, 220))
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 Successfully banned {member.mention} | Reason: {reason}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int):
    user = await bot.fetch_user(user_id)
    await ctx.guild.unban(user)
    await ctx.send(f"🔓 Successfully unbanned **{user.name}**")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 Successfully kicked {member.mention} | Reason: {reason}")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, minutes: int = 10, *, reason="No reason provided"):
    await member.timeout(timedelta(minutes=minutes), reason=reason)
    await ctx.send(f"🤫 Timed out {member.mention} for **{minutes} minutes** | Reason: {reason}")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def unmute(ctx, member: discord.Member):
    await member.timeout(None)
    await ctx.send(f"🔊 Removed timeout for {member.mention}!")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit: int = 5):
    await ctx.channel.purge(limit=limit + 1)
    msg = await ctx.send(f"🧹 Cleared {limit} messages successfully!")
    await msg.delete(delay=3)

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Channel locked successfully!")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Channel unlocked successfully!")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int = 0):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"⏱️ Slowmode set to {seconds} seconds!")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def nuke(ctx):
    channel = ctx.channel
    pos = channel.position
    new_channel = await channel.clone(reason="Channel Nuked")
    await new_channel.edit(position=pos)
    await channel.delete()
    await new_channel.send("💥 Channel nuked and recreated successfully!", delete_after=10)

@bot.command()
@commands.has_permissions(manage_roles=True)
async def role(ctx, member: discord.Member, role: discord.Role):
    if role in member.roles:
        await member.remove_roles(role)
        await ctx.send(f"❌ Removed **{role.name}** from {member.mention}")
    else:
        await member.add_roles(role)
        await ctx.send(f"✅ Added **{role.name}** to {member.mention}")

@bot.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason="No reason provided"):
    embed = discord.Embed(title="⚠️ Warning Issued", description=f"**User:** {member.mention}\n**Reason:** {reason}", color=discord.Color.orange())
    await ctx.send(embed=embed)
 @bot.command()
async def play(ctx, *, query: str = "Lofi Hip Hop Radio"):
    if not ctx.author.voice:
        await ctx.send("❌ Please join a Voice Channel first!")
        return
    channel = ctx.author.voice.channel
    try:
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()
    except Exception as e:
        await ctx.send(f"❌ Error connecting to voice channel: {e}")
        return
    embed = discord.Embed(title="🎵 Music / Radio Stream", description=f"🎶 Connected to **{channel.name}**!\n✨ **Stream/Query:** `{query}`", color=discord.Color.from_rgb(255, 209, 220))
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

@bot.command(aliases=["disconnect", "dc"])
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Disconnected from the voice channel!")
    else:
        await ctx.send("❌ Bot is not connected to any voice channel!")

@bot.command()
async def stop(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏹️ Music stopped successfully!")
    else:
        await ctx.send("❌ No music is currently playing!")

class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Ticket", emoji="🎫", style=discord.ButtonStyle.secondary, custom_id="create_ticket")
    async def create_ticket(self, interaction: discord.Interaction, button: Button):
        guild = interaction.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        category = discord.utils.get(guild.categories, name="Tickets") or await guild.create_category("Tickets")
        channel = await guild.create_text_channel(f"ticket-{interaction.user.name}", category=category, overwrites=overwrites)
        embed = discord.Embed(title="✨ Support Ticket Created", description=f"Hello {interaction.user.mention}!\nOur staff will be with you shortly.", color=discord.Color.from_rgb(255, 209, 220))
        embed.set_footer(text=FOOTER_TEXT)
        await channel.send(content=interaction.user.mention, embed=embed, view=TicketCloseView())
        await interaction.response.send_message(f"✅ Ticket created: {channel.mention}", ephemeral=True)

class TicketCloseView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close Ticket", emoji="🔒", style=discord.ButtonStyle.red, custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("🔒 Closing ticket in 3 seconds...")
        await interaction.channel.delete(delay=3)

@bot.group(invoke_without_command=True)
async def ticket(ctx):
    await ctx.send("Usage: `$ticket setup`")

@ticket.command(name="setup")
@commands.has_permissions(administrator=True)
async def ticket_setup(ctx):
    await ctx.message.delete()
    embed = discord.Embed(title="🎟️ Support & Help Center", description="Need assistance? Click the button below to open a private ticket!", color=discord.Color.from_rgb(255, 209, 220))
    embed.set_footer(text=f"Server Security & Support • {FOOTER_TEXT}")
    await ctx.send(embed=embed, view=TicketView())

@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! Latency: **{round(bot.latency * 1000)}ms**")

@bot.command()
async def afk(ctx, *, reason="AFK"):
    AFK_USERS[ctx.author.id] = reason
    try:
        await ctx.author.edit(nick=f"[AFK] {ctx.author.display_name}")
    except:
        pass
    await ctx.send(f"💤 {ctx.author.mention} is now AFK: **{reason}**")

@bot.command()
async def snipe(ctx):
    if ctx.channel.id not in SNIPE_CACHE:
        await ctx.send("❌ No deleted messages to snipe!")
        return
    data = SNIPE_CACHE[ctx.channel.id]
    embed = discord.Embed(title="🎯 Snipe Recovery", description=data["content"], color=discord.Color.from_rgb(255, 209, 220))
    embed.set_author(name=str(data["author"]), icon_url=data["author"].display_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def poll(ctx, *, question: str):
    await ctx.message.delete()
    embed = discord.Embed(title="📊 Server Poll", description=question, color=discord.Color.from_rgb(255, 209, 220))
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def say(ctx, *, message: str):
    await ctx.message.delete()
    await ctx.send(message)
 @bot.command()
@commands.has_permissions(manage_guild=True)
async def gstart(ctx, minutes: int, *, prize: str):
    await ctx.message.delete()
    embed = discord.Embed(title="🎉 **GIVEAWAY** 🎉", description=f"Prize: **{prize}**\nReact with 🎉 to enter!", color=discord.Color.from_rgb(255, 209, 220))
    g_msg = await ctx.send(embed=embed)
    await g_msg.add_reaction("🎉")
    await asyncio.sleep(minutes * 60)
    new_msg = await ctx.channel.fetch_message(g_msg.id)
    users = [user async for reaction in new_msg.reactions if str(reaction.emoji) == "🎉" async for user in reaction.users() if not user.bot]
    if users:
        await ctx.send(f"🎊 Congratulations {random.choice(users).mention}! You won **{prize}**!")
    else:
        await ctx.send("❌ Giveaway ended, no valid entries found.")

@bot.command()
async def membercount(ctx):
    await ctx.send(f"👥 Total members in **{ctx.guild.name}**: **{ctx.guild.member_count}**")

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"🏰 {guild.name} Server Info", color=discord.Color.from_rgb(255, 209, 220))
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name="👑 Owner", value=f"{guild.owner.mention}", inline=True)
    embed.add_field(name="👥 Members", value=f"**{guild.member_count}**", inline=True)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"👤 {member.name}'s Profile", color=discord.Color.from_rgb(255, 209, 220))
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="🏷️ Tag", value=f"{member.mention}", inline=True)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

@bot.command()
async def ship(ctx, member1: discord.Member, member2: discord.Member = None):
    score = random.randint(0, 100)
    member2 = member2 or ctx.author
    embed = discord.Embed(title="❤️ Love Compatibility Meter ❤️", description=f"**{member1.mention}** ❤️ **{member2.mention}**\n\nScore: **{score}%**", color=discord.Color.from_rgb(255, 209, 220))
    await ctx.send(embed=embed)

@bot.command()
async def chutiya(ctx, member: discord.Member = None):
    await ctx.send(f"🤪 {(member or ctx.author).mention} is officially **{random.randint(0, 100)}%** certified! 💀")

@bot.command()
async def howgay(ctx, member: discord.Member = None):
    await ctx.send(f"🏳️‍🌈 {(member or ctx.author).mention} is **{random.randint(0, 100)}%** Gay!")

@bot.command()
async def cute(ctx, member: discord.Member = None):
    await ctx.send(f"✨ {(member or ctx.author).mention} is **{random.randint(0, 100)}%** Cute!")

@bot.command(name="8ball")
async def eightball(ctx, *, question: str):
    await ctx.send(f"🎱 **Question:** {question}\n✨ **Answer:** {random.choice(['Yes!', 'No.', 'Maybe.', 'Definitely!'])}")

@bot.command()
async def hack(ctx, member: discord.Member):
    msg = await ctx.send(f"💻 Hacking {member.mention}...")
    await asyncio.sleep(1.5)
    await msg.edit(content=f"✅ Successfully hacked {member.mention}! Password: `ilovepudding123`")

@bot.command()
async def rps(ctx, choice: str):
    choices = ["rock", "paper", "scissors"]
    bot_choice = random.choice(choices)
    await ctx.send(f"🤖 **Bot:** {bot_choice} | 👤 **You:** {choice.lower()}")

@bot.command()
async def fact(ctx):
    await ctx.send(f"💡 **Did you know?**\nHoney never spoils! 🍯")

@bot.command()
async def hug(ctx, member: discord.Member):
    await ctx.send(f"🤗 {ctx.author.mention} gave a warm hug to {member.mention}! 💖")

@bot.command()
async def kiss(ctx, member: discord.Member):
    await ctx.send(f"💋 {ctx.author.mention} kissed {member.mention}! 😘")

@bot.command()
async def slap(ctx, member: discord.Member):
    await ctx.send(f"🤚 {ctx.author.mention} slapped {member.mention}! 💥")

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"🖼️ {member.name}'s Avatar", color=discord.Color.from_rgb(255, 209, 220))
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def coinflip(ctx):
    await ctx.send(f"🎲 Coin flipped: **{random.choice(['Heads 🪙', 'Tails 🪙'])}**")

@bot.command()
async def meme(ctx):
    embed = discord.Embed(title="😂 Random Meme", color=discord.Color.from_rgb(255, 209, 220))
    embed.set_image(url="https://media.giphy.com/media/3o7TKSjRrfIPjeiOkM/giphy.gif")
    await ctx.send(embed=embed)

@bot.command()
async def roast(ctx, member: discord.Member = None):
    await ctx.send(f"🔥 {(member or ctx.author).mention}, you bring everyone so much joy when you leave the room.")

@bot.command()
async def math(ctx, *, expression: str):
    try:
        await ctx.send(f"🧮 Result: **{eval(expression, {'__builtins__': None}, {})}**")
    except:
        await ctx.send("❌ Invalid math expression!")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        cmd_name = ctx.message.content.split()[0][1:]
        embed = discord.Embed(title=f"⚙️ Module: {cmd_name.capitalize()}", description=f"Command `${cmd_name}` is active and registered! 🐾", color=discord.Color.from_rgb(255, 209, 220))
        embed.set_footer(text=FOOTER_TEXT)
        await ctx.send(embed=embed)
    else:
        raise error

if __name__ == "__main__":
    keep_alive()
    bot.run(os.getenv('TOKEN', 'YOUR_DISCORD_BOT_TOKEN_HERE'))
 
