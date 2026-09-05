 import os
import random
import urllib.parse
from datetime import timedelta
import discord
from discord.ext import commands
from discord.ui import Select, View, Button
from flask import Flask
from threading import Thread

# ==================== KEEP-ALIVE (24/7 UPTIME) ====================
app = Flask('')

@app.route('/')
def home():
    return "Pudding Bot is online and running 24/7! 🐾"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# ==================== BOT SETUP ====================
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents, help_command=None)

# Global stores
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

    # Check for AFK status removal
    if message.author.id in AFK_USERS:
        reason = AFK_USERS.pop(message.author.id)
        try:
            await message.author.edit(nick=message.author.display_name.replace("[AFK] ", ""))
        except:
            pass
        await message.channel.send(f"👋 Welcome back {message.author.mention}, I removed your AFK status!", delete_after=5)

    # Check for AFK pings
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
            discord.SelectOption(label="Ticket", emoji="🎟️", description="Ticket system controls"),
            discord.SelectOption(label="Fun & Roleplay", emoji="⚛️", description="Fun & Roleplay commands"),
            discord.SelectOption(label="General", emoji="👻", description="General server utility"),
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
        elif val == "Ticket":
            embed.title = "🎟️ Ticket Module"
            embed.add_field(name="Commands", value="`$ticket setup`, `$ticket close`, `$ticket delete`", inline=False)
        elif val == "Fun & Roleplay":
            embed.title = "⚛️ Fun & Roleplay Module"
            embed.add_field(name="Commands", value="`$howgay`, `$cute`, `$8ball`, `$hug`, `$kiss`, `$slap`", inline=False)
        elif val == "General":
            embed.title = "👻 General Module"
            embed.add_field(name="Commands", value="`$ping`, `$afk`, `$avatar`, `$servericon`, `$serverinfo`, `$userinfo`, `$membercount`, `$snipe`", inline=False)

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
        description=f"• **Prefix:** `$`\n• **Support:** [Join Server]({SUPPORT_SERVER_LINK})",
        color=discord.Color.from_rgb(255, 209, 220)
    )
    embed.set_thumbnail(url=bot.user.display_avatar.url)
    embed.add_field(name="Categories", value="⚔️ Antinuke\n⚒️ Moderation\n🎟️ Tickets\n🎮 Fun & Roleplay\n👻 General", inline=False)
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

# ==================== UTILITY & GENERAL COMMANDS ====================
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
async def servericon(ctx):
    if not ctx.guild.icon:
        await ctx.send("❌ This server doesn't have an icon!")
        return
    embed = discord.Embed(title=f"🖼️ {ctx.guild.name} Icon", color=discord.Color.from_rgb(255, 209, 220))
    embed.set_image(url=ctx.guild.icon.url)
    await ctx.send(embed=embed)

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

# ==================== DYNAMIC UPI PAYMENT / QR ====================
@bot.command(aliases=["qr", "payment", "upi"])
async def pay(ctx, amount: str = None, *, reason: str = "General Payment"):
    if amount is None:
        await ctx.send("❌ Usage: `$pay <amount> [reason]`\n**Example:** `$pay 100 Subscription`")
        return

    upi_id = "ankittt.3@fam"
    name = "Ankit"
    encoded_reason = urllib.parse.quote(reason)
    
    upi_url = f"upi://pay?pa={upi_id}&pn={urllib.parse.quote(name)}&am={amount}&cu=INR&tn={encoded_reason}"
    qr_api_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={urllib.parse.quote(upi_url)}"

    embed = discord.Embed(
        title="💳 Dynamic UPI Payment",
        description=f"Payment request generated for {ctx.author.mention}",
        color=discord.Color.from_rgb(255, 209, 220)
    )
    
    embed.add_field(name="💰 Amount", value=f"**₹{amount}**", inline=True)
    embed.add_field(name="📌 Reason", value=f"**{reason}**", inline=True)
    embed.add_field(name="🌐 UPI ID", value=f"`{upi_id}`", inline=False)
    
    embed.set_image(url=qr_api_url)
    embed.set_footer(text=FOOTER_TEXT, icon_url=bot.user.display_avatar.url)
    
    view = View()
    view.add_item(Button(label="Pay Now (UPI)", emoji="📲", url=upi_url))
    
    await ctx.send(embed=embed, view=view)

# ==================== FUN & ROLEPLAY COMMANDS ====================
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
     
