 import os
import random
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

# ==================== CONFIGURATION ====================
FOOTER_TEXT = "Developer: ADX ANKIT | Pudding 🐾"
SUPPORT_SERVER_LINK = "https://discord.gg/Yttbf69xx"
QR_IMAGE_URL = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Pudding Bot is active across servers! 🐾")
    activity = discord.Activity(type=discord.ActivityType.streaming, name="🍮 Baking cute servers | $help 🐾", url="https://twitch.tv/discord")
    await bot.change_presence(status=discord.Status.online, activity=activity)

# ==================== HELP MENU SYSTEM ====================
class HelpDropdown(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Antinuke", emoji="🛡️", description="Antinuke & MainRole commands"),
            discord.SelectOption(label="Moderation", emoji="⚒️", description="Moderation, Purge & Jail"),
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
            embed.add_field(name="Commands", value="`$ban`, `$unban`, `$kick`, `$mute`, `$unmute`, `$purge`, `$lock`, `$unlock`", inline=False)
        elif val == "Ticket":
            embed.title = "🎟️ Ticket Module"
            embed.add_field(name="Commands", value="`$ticket setup`, `$ticket panel`, `$ticket close`, `$ticket delete`", inline=False)
        elif val == "Fun & Roleplay":
            embed.title = "⚛️ Fun Module"
            embed.add_field(name="Commands", value="`$howgay`, `$cute`, `$translate`, `$horny`, `$hug`, `$kiss`, `$slap`", inline=False)
        elif val == "General":
            embed.title = "👻 General Module"
            embed.add_field(name="Commands", value="`$afk`, `$avatar`, `$banner`, `$servericon`, `$membercount`", inline=False)

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

# ==================== MODERATION COMMANDS ====================
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 Successfully banned {member.mention} | Reason: {reason}")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 Successfully kicked {member.mention} | Reason: {reason}")

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

# ==================== UTILITY & FUN ====================
@bot.command(aliases=["qr", "payment", "upi"])
async def pay(ctx, amount: str = None, *, reason: str = "General Payment"):
    if amount is None:
        await ctx.send("❌ Usage: `$pay <amount> [reason]`")
        return
    embed = discord.Embed(title="💳 Payment Invoice", color=discord.Color.from_rgb(255, 209, 220))
    embed.add_field(name="💰 Amount", value=f"**₹{amount}**", inline=True)
    embed.add_field(name="📌 Reason", value=f"**{reason}**", inline=True)
    embed.add_field(name="🌐 UPI ID", value="`ankittt.3@fam`", inline=False)
    embed.set_image(url=QR_IMAGE_URL)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

@bot.command()
async def howgay(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(f"🏳️‍🌈 {member.mention} is **{random.randint(0, 100)}%** Gay!")

@bot.command()
async def cute(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(f"✨ {member.mention} is **{random.randint(0, 100)}%** Cute!")

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
