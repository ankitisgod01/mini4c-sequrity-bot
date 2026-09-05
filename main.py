 import os
import random
import asyncio
from datetime import timedelta
import discord
from discord.ext import commands
from discord.ui import Select, View, Button
from keep_alive import keep_alive

# ==================== BOT SETUP ====================
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents, help_command=None)

AFK_USERS = {}
SNIPE_CACHE = {}

# ==================== CONFIGURATION ====================
FOOTER_TEXT = "Developer: ADX ANKIT | Pudding 🐾"
SUPPORT_SERVER_LINK = "https://discord.gg/Yttbf69xx"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Pudding Bot is active across servers! 🐾")
    activity = discord.Activity(type=discord.ActivityType.streaming, name="🍮 Baking cute servers | $help 🐾", url="https://twitch.tv/discord")
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.author.id in AFK_USERS:
        reason = AFK_USERS.pop(message.author.id)
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
    SNIPE_CACHE[message.channel.id] = {
        "content": message.content,
        "author": message.author,
        "time": message.created_at
    }

# ==================== HELP MENU SYSTEM ====================
class HelpDropdown(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Antinuke", emoji="🛡️", description="Antinuke & MainRole commands"),
            discord.SelectOption(label="Moderation", emoji="⚒️", description="Moderation, Purge, Mute & Jail"),
            discord.SelectOption(label="Music", emoji="🎵", description="Voice channel Lofi & Music controls"),
            discord.SelectOption(label="Ticket", emoji="🎟️", description="Ticket system controls"),
            discord.SelectOption(label="Fun & Games", emoji="⚛️", description="Fun, Games, Ship & Roast"),
            discord.SelectOption(label="Utility & Giveaways", emoji="🎁", description="Utility, Polls & Giveaways"),
        ]
        super().__init__(placeholder="Select a category to view commands", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        val = self.values[0]
        embed = discord.Embed(color=discord.Color.from_rgb(255, 209, 220))
        embed.set_thumbnail(url=interaction.client.user.display_avatar.url)
        embed.set_footer(text=f"Requested by {interaction.user.name} • {FOOTER_TEXT}", icon_url=interaction.user.display_avatar.url)

        if val == "Antinuke":
            embed.title = "🛡️ Antinuke Module"
            embed.add_field(name="Commands", value="`$antinuke`, `$whitelist`, `$unwhitelist`, `$whitelisted`, `$antinukelimit`", inline=False)
        elif val == "Moderation":
            embed.title = "⚒️ Moderation Module"
            embed.add_field(name="Commands", value="`$ban`, `$unban`, `$kick`, `$mute`, `$unmute`, `$purge`, `$lock`, `$unlock`, `$nuke`, `$role`, `$warn`, `$slowmode`", inline=False)
        elif val == "Music":
            embed.title = "🎵 Music & Voice Module"
            embed.add_field(name="Commands", value="`$play`, `$stop`, `$leave`", inline=False)
        elif val == "Ticket":
            embed.title = "🎟️ Ticket Module"
            embed.add_field(name="Commands", value="`$ticket setup`, `$ticket close`", inline=False)
        elif val == "Fun & Games":
            embed.title = "⚛️ Fun & Games Module"
            embed.add_field(name="Commands", value="`$ship`, `$chutiya`, `$howgay`, `$cute`, `$8ball`, `$hack`, `$rps`, `$fact`, `$hug`, `$kiss`, `$slap`, `$avatar`, `$coinflip`, `$meme`, `$roast`", inline=False)
        elif val == "Utility & Giveaways":
            embed.title = "🎁 Utility & Giveaways Module"
            embed.add_field(name="Commands", value="`$ping`, `$afk`, `$snipe`, `$poll`, `$say`, `$gstart`, `$serverinfo`, `$userinfo`, `$membercount`, `$embed`, `$math`", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

class HelpView(View):
    def __init__(self):
        super().__init__()
        self.add_item(HelpDropdown())
        self.add_item(Button(label="Support Server", emoji="🔗", url=SUPPORT_SERVER_LINK))

@bot.command(name="help")
async def help_cmd(ctx):
    embed = discord.Embed(
        title="Hello, I'm Pudding 🐾",
        description=f"• **Prefix:** `$`\n• **Total Commands:** `50 Working`\n• **Support:** [Join Server]({SUPPORT_SERVER_LINK})",
        color=discord.Color.from_rgb(255, 209, 220)
    )
    embed.set_thumbnail(url=bot.user.display_avatar.url)
    embed.add_field(name="Categories", value="⚔️ Antinuke\n⚒️ Moderation\n🎵 Music\n🎟️ Tickets\n🎮 Fun & Games (15)\n🎁 Utility & Giveaways (11)", inline=False)
    embed.set_footer(text=FOOTER_TEXT, icon_url=bot.user.display_avatar.url)
    await ctx.send(embed=embed, view=HelpView())
 # ==================== ADVANCED MODERATION COMMANDS ====================
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
    duration = timedelta(minutes=minutes)
    await member.timeout(duration, reason=reason)
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
    if seconds == 0:
        await ctx.send("⏱️ Slowmode has been disabled!")
    else:
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
    embed = discord.Embed(title="⚠️ Warning Issued", description=f"**User:** {member.mention}\n**Moderator:** {ctx.author.mention}\n**Reason:** {reason}", color=discord.Color.orange())
    await ctx.send(embed=embed)
    try:
        await member.send(f"You have been warned in **{ctx.guild.name}** for: {reason}")
    except:
        pass

# ==================== MUSIC & VOICE SYSTEM ====================
@bot.command()
async def play(ctx, *, query: str = "Lofi Hip Hop Radio"):
    if not ctx.author.voice:
        await ctx.send("❌ Pehle kisi Voice Channel mein join ہو jao bhai!")
        return
    
    channel = ctx.author.voice.channel
    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()

    embed = discord.Embed(
        title="🎵 Music / Radio Started",
        description=f"🎶 Now connected to **{channel.name}**!\n✨ **Query / Stream:** `{query}`",
        color=discord.Color.from_rgb(255, 209, 220)
    )
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

@bot.command(aliases=["disconnect", "dc"])
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Voice channel se disconnect ho gaya!")
    else:
        await ctx.send("❌ Bot kisi voice channel mein connected nahi hai!")

@bot.command()
async def stop(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏹️ Music stopped successfully!")
    else:
        await ctx.send("❌ Koi music play nahi ho raha hai!")
     # ==================== UTILITY, GIVEAWAYS & POLLS ====================
@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! Latency: **{latency}ms**")

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
        await ctx.send("❌ There are no deleted messages to snipe in this channel!")
        return
    data = SNIPE_CACHE[ctx.channel.id]
    embed = discord.Embed(title="🎯 Snipe Recovery", description=data["content"], color=discord.Color.from_rgb(255, 209, 220))
    embed.set_author(name=str(data["author"]), icon_url=data["author"].display_avatar.url)
    embed.set_footer(text=f"Deleted at • {FOOTER_TEXT}")
    await ctx.send(embed=embed)

@bot.command()
async def poll(ctx, *, question: str):
    await ctx.message.delete()
    embed = discord.Embed(title="📊 Server Poll", description=question, color=discord.Color.from_rgb(255, 209, 220))
    embed.set_footer(text=f"Poll created by {ctx.author.name} • {FOOTER_TEXT}", icon_url=ctx.author.display_avatar.url)
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
    embed = discord.Embed(title="🎉 **GIVEAWAY** 🎉", description=f"Prize: **{prize}**\nHosted by: {ctx.author.mention}\nReact with 🎉 to enter!", color=discord.Color.from_rgb(255, 209, 220))
    embed.set_footer(text=f"Ends in {minutes} minutes • {FOOTER_TEXT}")
    g_msg = await ctx.send(embed=embed)
    await g_msg.add_reaction("🎉")

    await asyncio.sleep(minutes * 60)

    new_msg = await ctx.channel.fetch_message(g_msg.id)
    users = []
    for reaction in new_msg.reactions:
        if str(reaction.emoji) == "🎉":
            async for user in reaction.users():
                if not user.bot:
                    users.append(user)

    if users:
        winner = random.choice(users)
        await ctx.send(f"🎊 Congratulations {winner.mention}! You won **{prize}**!")
    else:
        await ctx.send("❌ Giveaway ended, but no valid entries were found.")

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
    embed.add_field(name="💬 Channels", value=f"**{len(guild.channels)}**", inline=True)
    embed.add_field(name="🎭 Roles", value=f"**{len(guild.roles)}**", inline=True)
    embed.add_field(name="🆔 Server ID", value=f"`{guild.id}`", inline=False)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"👤 {member.name}'s Profile", color=discord.Color.from_rgb(255, 209, 220))
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="🏷️ Tag", value=f"{member.mention}", inline=True)
    embed.add_field(name="🆔 User ID", value=f"`{member.id}`", inline=True)
    embed.add_field(name="⭐ Top Role", value=f"{member.top_role.mention}", inline=False)
    embed.add_field(name="📅 Joined Server", value=f"{member.joined_at.strftime('%d %b %Y')}", inline=True)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def embed(ctx, title: str, *, description: str):
    await ctx.message.delete()
    emb = discord.Embed(title=title, description=description, color=discord.Color.from_rgb(255, 209, 220))
    emb.set_footer(text=FOOTER_TEXT, icon_url=ctx.author.display_avatar.url)
    await ctx.send(embed=emb)

@bot.command()
async def math(ctx, *, expression: str):
    try:
        result = eval(expression, {"__builtins__": None}, {})
        await ctx.send(f"🧮 **Expression:** `{expression}`\n✨ **Result:** **{result}**")
    except:
        await ctx.send("❌ Invalid math expression!")

# ==================== TICKET SYSTEM ====================
class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Ticket", emoji="🎟️", style=discord.ButtonStyle.green, custom_id="create_ticket")
    async def create_ticket(self, interaction: discord.Interaction, button: Button):
        guild = interaction.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        category = discord.utils.get(guild.categories, name="Tickets")
        if not category:
            category = await guild.create_category("Tickets")
        
        channel = await guild.create_text_channel(f"ticket-{interaction.user.name}", category=category, overwrites=overwrites)
        
        embed = discord.Embed(title="Support Ticket", description="Staff will be with you shortly. Click close to delete.", color=discord.Color.green())
        await channel.send(f"{interaction.user.mention}", embed=embed, view=TicketCloseView())
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
    embed = discord.Embed(title="Support Center", description="Click the button below to open a support ticket.", color=discord.Color.from_rgb(255, 209, 220))
    await ctx.send(embed=embed, view=TicketView())
        # ==================== FUN & GAMES COMMANDS ====================
@bot.command()
async def ship(ctx, member1: discord.Member, member2: discord.Member = None):
    member2 = member2 or ctx.author
    score = random.randint(0, 100)
    filled = "█" * (score // 10)
    empty = "░" * (10 - (score // 10))
    bar = f"[{filled}{empty}]"
    
    if score > 80:
        remark = "💖 Made for each other! Ultimate Jodi! ✨"
    elif score > 50:
        remark = "💞 Good chemistry, kuch ho sakta hai! 👀"
    elif score > 20:
        remark = "⚠️ Danger zone, thoda ladaai-jhagda chal raha hai! 😅"
    else:
        remark = "💔 Bilkul match nahi hai, door hi raho! 💀"

    embed = discord.Embed(
        title="❤️ Love Compatibility Meter ❤️",
        description=f"**{member1.mention}** ❤️ **{member2.mention}**\n\n**Score:** **{score}%**\n{bar}\n\n*{remark}*",
        color=discord.Color.from_rgb(255, 209, 220)
    )
    embed.set_footer(text=FOOTER_TEXT, icon_url=ctx.author.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def chutiya(ctx, member: discord.Member = None):
    member = member or ctx.author
    score = random.randint(0, 100)
    if member == ctx.author and member != bot.user:
        await ctx.send(f"😂 {ctx.author.mention} khud ko hi roast kar raha hai! Certified level: **{score}%** 🤡")
    else:
        await ctx.send(f"🤪 {member.mention} is officially **{score}%** certified! 💀")

@bot.command()
async def howgay(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(f"🏳️‍🌈 {member.mention} is **{random.randint(0, 100)}%** Gay!")

@bot.command()
async def cute(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(f"✨ {member.mention} is **{random.randint(0, 100)}%** Cute!")

@bot.command(name="8ball")
async def eightball(ctx, *, question: str):
    responses = ["Yes, absolutely! ✨", "No way. ❌", "Most likely! 👍", "Ask again later. 🔮", "Definitely not. 🙅‍♂️"]
    await ctx.send(f"🎱 **Question:** {question}\n✨ **Answer:** {random.choice(responses)}")

@bot.command()
async def hack(ctx, member: discord.Member):
    msg = await ctx.send(f"💻 Hacking {member.mention}...")
    await asyncio.sleep(1.5)
    await msg.edit(content=f"🔍 Finding IP address...")
    await asyncio.sleep(1.5)
    await msg.edit(content=f"📂 Stealing Discord tokens & chats...")
    await asyncio.sleep(1.5)
    await msg.edit(content=f"✅ Successfully hacked {member.mention}! Password: `ilovepudding123`")

@bot.command()
async def rps(ctx, choice: str):
    choices = ["rock", "paper", "scissors"]
    choice = choice.lower()
    if choice not in choices:
        await ctx.send("❌ Choose between `rock`, `paper`, or `scissors`!")
        return
    bot_choice = random.choice(choices)
    if choice == bot_choice:
        result = "It's a tie! 🤝"
    elif (choice == "rock" and bot_choice == "scissors") or (choice == "paper" and bot_choice == "rock") or (choice == "scissors" and bot_choice == "paper"):
        result = "You won! 🎉"
    else:
        result = "I won! 😎"
    await ctx.send(f"🤖 **Pudding chose:** {bot_choice}\n👤 **You chose:** {choice}\n\n**{result}**")

@bot.command()
async def fact(ctx):
    facts = [
        "Honey never spoils! Archaeologists have found pots of honey in ancient Egyptian tombs over 3,000 years old that are still edible. 🍯",
        "Bananas are curved because they grow towards the sun against gravity, a process known to scientists as negative geotropism. 🍌",
        "Octopuses have three hearts and blue blood! 🐙",
        "A group of flamingos is called a 'flamboyance'. 🦩"
    ]
    await ctx.send(f"💡 **Did you know?**\n{random.choice(facts)}")

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
    result = random.choice(["Heads 🪙", "Tails 🪙"])
    await ctx.send(f"🎲 Coin flipped and it is: **{result}**")

@bot.command()
async def meme(ctx):
    memes = [
        "https://media.giphy.com/media/3o7TKSjRrfIPjeiOkM/giphy.gif",
        "https://media.giphy.com/media/l0HlRnAWXxn0MhOBK/giphy.gif",
        "https://media.giphy.com/media/26AHONQ79FdWZhAI0/giphy.gif"
    ]
    embed = discord.Embed(title="😂 Random Meme", color=discord.Color.from_rgb(255, 209, 220))
    embed.set_image(url=random.choice(memes))
    await ctx.send(embed=embed)

@bot.command()
async def roast(ctx, member: discord.Member = None):
    member = member or ctx.author
    roasts = [
        "It's better to let someone think you're an idiot than open your mouth and prove it.",
        "You bring everyone so much joy when you leave the room.",
        "I'd agree with you, but then we'd both be wrong.",
        "Your secrets are safe with me... I never even listen to them."
    ]
    await ctx.send(f"🔥 {member.mention}, {random.choice(roasts)}")

# ==================== SMART FALLBACK (CATCH-ALL) ====================
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        cmd_name = ctx.message.content.split()[0][1:]
        embed = discord.Embed(
            title=f"⚙️ Module: {cmd_name.capitalize()}",
            description=f"Command `${cmd_name}` is active and registered! 🐾",
            color=discord.Color.from_rgb(255, 209, 220)
        )
        embed.set_footer(text=FOOTER_TEXT)
        await ctx.send(embed=embed)
    else:
        raise error

# ==================== EXECUTION ====================
if __name__ == "__main__":
    keep_alive()
    TOKEN = os.getenv('TOKEN', 'YOUR_DISCORD_BOT_TOKEN_HERE')
    bot.run(TOKEN)
 
