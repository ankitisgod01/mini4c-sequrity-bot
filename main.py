import os
import random
import discord
from discord.ext import commands
from discord.ui import Select, View, Button

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents, help_command=None)

# ==================== CONFIGURATION ====================
OWNER_IDS = [123456789012345678]  # Replace with your Discord User ID
FOOTER_TEXT = "Developer: ADX ANKIT | MINI4C X SEQURITY ⚡"
SUPPORT_SERVER_LINK = "https://discord.gg/Yttbf69xx"
QR_IMAGE_URL = "HTTPS_LINK_TO_YOUR_QR_IMAGE"  # Replace with your QR Code Image URL

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    
    activity = discord.Activity(
        type=discord.ActivityType.watching, 
        name="$help | Tera Baap Bhi Nahi Kar Payega Nuke ⚡💀🔥"
    )
    await bot.change_presence(status=discord.Status.dnd, activity=activity)

# ==================== HELP MENU SYSTEM ====================

class HelpDropdown(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Antinuke", emoji="🛡️", description="Antinuke & MainRole commands"),
            discord.SelectOption(label="AutoMod", emoji="🤖", description="AutoMod & Antibot commands"),
            discord.SelectOption(label="Automations", emoji="🔗", description="Autorole & Server automations"),
            discord.SelectOption(label="Autoresponder", emoji="💬", description="Autoresponder & Autoreact"),
            discord.SelectOption(label="CustomRole", emoji="🤌", description="Custom roles management"),
            discord.SelectOption(label="Fun & Roleplay", emoji="⚛️", description="Fun & Roleplay commands"),
            discord.SelectOption(label="General", emoji="👻", description="General server utility"),
            discord.SelectOption(label="Giveaway", emoji="🎁", description="Giveaway management"),
            discord.SelectOption(label="Logging", emoji="🕶️", description="Server activity logs"),
            discord.SelectOption(label="Moderation & Jail", emoji="⚒️", description="Moderation, Purge & Jail"),
            discord.SelectOption(label="Permit & Ignore", emoji="👑", description="Extraowner & Ignore list"),
            discord.SelectOption(label="Ticket", emoji="🎟️", description="Ticket system controls"),
            discord.SelectOption(label="Welcomer", emoji="🚪", description="Greet & Welcome settings"),
        ]
        super().__init__(placeholder="Select a category to view commands", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        val = self.values[0]
        embed = discord.Embed(color=discord.Color.from_rgb(47, 49, 54))
        embed.set_thumbnail(url=interaction.client.user.display_avatar.url)
        embed.set_footer(text=f"Requested by {interaction.user.name} • {FOOTER_TEXT}", icon_url=interaction.user.display_avatar.url)

        if val == "Antinuke":
            embed.title = "🛡️ Antinuke Module"
            embed.add_field(name="Antinuke Commands", value="`antinuke`, `whitelist`, `unwhitelist`, `whitelisted`, `whitelist reset`, `antinukelimit`, `antinukepunishment`, `antinukeconfig`, `antinukereset`", inline=False)
            embed.add_field(name="MainRole Commands", value="`mainrole add`, `mainrole remove`, `mainrole list`, `mainrole reset`", inline=False)

        elif val == "AutoMod":
            embed.title = "🤖 AutoMod Module"
            embed.add_field(name="AutoMod Commands", value="`automod`, `automod enable`, `automod disable`, `automod punishment`, `automod config`, `automod logging`, `automod ignore`, `automod ignore channel`, `automod ignore role`, `automod ignore show`, `automod ignore reset`, `automod unignore`, `automod unignore channel`, `automod unignore role`", inline=False)
            embed.add_field(name="Antibot Commands", value="`antibot`, `antibot add`, `antibot remove`, `antibot wl`, `antibot config`, `antibot reset`", inline=False)

        elif val == "Automations":
            embed.title = "🔗 Automations Module"
            embed.add_field(name="Autorole Commands", value="`autorole`, `autorole bots add`, `autorole bots remove`, `autorole bots`, `autorole config`, `autorole humans add`, `autorole humans remove`, `autorole humans`, `autorole reset all`, `autorole reset bots`, `autorole reset humans`", inline=False)

        elif val == "Autoresponder":
            embed.title = "💬 Autoresponder Module"
            embed.add_field(name="Autoresponder Commands", value="`autoresponder`, `autoresponder create`, `autoresponder delete`, `autoresponder edit`, `autoresponder config`", inline=False)
            embed.add_field(name="Autoreact Commands", value="`react`, `react add`, `react remove`, `react list`, `react reset`", inline=False)

        elif val == "CustomRole":
            embed.title = "🤌 CustomRole Module"
            embed.add_field(name="CustomRole Commands", value="`setup`, `setup create`, `setup delete`, `setup list`, `setup staff`, `setup girl`, `setup friend`, `setup vip`, `setup guest`, `setup config`, `setup reset`, `staff`, `girl`, `friend`, `vip`, `guest`", inline=False)

        elif val == "Fun & Roleplay":
            embed.title = "⚛️ Fun & Roleplay Module"
            embed.add_field(name="Fun Commands", value="`translate`, `howgay`, `lesbian`, `cute`, `intelligence`, `chutiya`, `horny`, `tharki`, `gif`, `weather`, `fakeban`, `image`, `8ball`, `truth`, `dare`", inline=False)
            embed.add_field(name="Roleplay Commands", value="`hug`, `kiss`, `pat`, `cuddle`, `slap`, `tickle`, `spank`, `kill`, `poke`, `highfive`, `bite`, `bonk`, `punch`, `stare`, `wave`, `smug`, `yeet`, `dance`, `handhold`, `cry`, `lappillow`, `happy`", inline=False)

        elif val == "General":
            embed.title = "👻 General Module"
            embed.add_field(name="General Commands", value="`status`, `afk`, `avatar`, `banner`, `servericon`, `membercount`, `poll`, `wizz`, `urban`, `users`, `list boosters`, `list inrole`, `list emojis`, `list bots`, `list admins`, `list invoice`, `list early`, `list roles`", inline=False)

        elif val == "Giveaway":
            embed.title = "🎁 Giveaway Module"
            embed.add_field(name="Giveaway Commands", value="`gstart`, `gend`, `greroll`, `glist`, `gstaff role`, `gstaff reset`, `gconfig`, `gembed set`, `gembed reset`", inline=False)

        elif val == "Logging":
            embed.title = "🕶️ Logging Module"
            embed.add_field(name="Logging Commands", value="`logging`, `logging setup`, `logging auto`, `logging config`, `logging enable`, `logging disable`, `logging reset`", inline=False)

        elif val == "Moderation & Jail":
            embed.title = "⚒️ Moderation & Jail Module"
            embed.add_field(name="Moderation Commands", value="`ban`, `unban`, `unbanall`, `kick`, `mute`, `unmute`, `unmuteall`, `warn`, `clearwarns`, `lock`, `lockall`, `unlock`, `unlockall`, `hide`, `hideall`, `unhide`, `unhideall`, `nick`, `nuke`, `clone`, `snipe`, `slowmode`, `unslowmode`, `enlarge`, `steal`, `role`, `role create`, `role delete`, `role rename`, `role all`, `role humans`, `role bots`, `role unverified`, `removerole`, `rrole all`, `rrole humans`, `rrole bots`, `purge`, `purge embeds`, `purge files`, `purge images`, `purge bot`, `purge emoji`, `purge contains`, `purge reactions`, `purge user`", inline=False)
            embed.add_field(name="Jail Commands", value="`jail`, `unjail`, `jail setup`, `jail list`, `jail config`, `jail reset`", inline=False)

        elif val == "Permit & Ignore":
            embed.title = "👑 Permit & Ignore Module"
            embed.add_field(name="Permit Commands", value="`extraowner set`, `extraowner view`, `extraowner reset`", inline=False)
            embed.add_field(name="Ignore Commands", value="`ignore`, `ignore command add`, `ignore command remove`, `ignore command show`, `ignore channel add`, `ignore channel remove`, `ignore channel show`, `ignore user add`, `ignore user remove`, `ignore user show`, `ignore bypass add`, `ignore bypass show`, `ignore bypass remove`", inline=False)

        elif val == "Ticket":
            embed.title = "🎟️ Ticket Module"
            embed.add_field(name="Ticket Commands", value="`ticket`, `ticket setup`, `ticket panel`, `ticket staff`, `ticket setcategory`, `ticket transcript`, `ticket adduser`, `ticket removeuser`, `ticket close`, `ticket delete`, `ticket config`, `ticket reset`, `ticket edit`", inline=False)

        elif val == "Welcomer":
            embed.title = "🚪 Welcomer Module"
            embed.add_field(name="Welcomer Commands", value="`greet`, `greet setup`, `greet reset`, `greet channel`, `greet edit`, `greet test`, `greet config`, `greet autodelete`", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

class HelpView(View):
    def __init__(self):
        super().__init__()
        self.add_item(HelpDropdown())
        self.add_item(Button(label="Home", emoji="🏠", style=discord.ButtonStyle.secondary))
        self.add_item(Button(label="Support Server", emoji="🔗", url=SUPPORT_SERVER_LINK))

@bot.command(name="help")
async def help_cmd(ctx):
    embed = discord.Embed(
        title="Hello, I'm MINI4C X SEQURITY",
        description=(
            f"• **Prefix for this server:** `$`\n"
            f"• **Set prefix with:** `$prefix <new>`\n"
            f"• **Need help?** [Join Support Server]({SUPPORT_SERVER_LINK})"
        ),
        color=discord.Color.from_rgb(47, 49, 54)
    )
    embed.set_thumbnail(url=bot.user.display_avatar.url)
    
    categories = (
        "⚔️ » **Antinuke**\n⚒️ » **AutoMod**\n📡 » **Automations**\n📌 » **Logging**\n"
        "🔨 » **Moderation**\nℹ️ » **Information**\n💬 » **General**\n🌐 » **Social**\n"
        "🎮 » **Fun**\n🤍 » **Roleplay**\n🎟️ » **Tickets**\n🔔 » **Welcome & Greet**\n🎧 » **Join to Create**"
    )
    embed.add_field(name="\u200b", value=categories, inline=False)
    embed.set_footer(text=FOOTER_TEXT, icon_url=bot.user.display_avatar.url)
    
    await ctx.send(embed=embed, view=HelpView())

# ==================== PAYMENT / QR COMMAND ====================

@bot.command(aliases=["qr", "payment", "upi"])
async def pay(ctx, amount: str = None, *, reason: str = "General Payment"):
    if amount is None:
        embed = discord.Embed(
            title="❌ Missing Parameters",
            description="Please specify an amount to generate a payment invoice.\n\n**Usage:** `$pay <amount> [reason]`\n**Example:** `$pay 100 Bot Subscription`",
            color=discord.Color.red()
        )
        embed.set_footer(text=FOOTER_TEXT)
        await ctx.send(embed=embed)
        return

    embed = discord.Embed(
        title="💳 Payment Invoice",
        description=f"Payment request generated for {ctx.author.mention}",
        color=discord.Color.from_rgb(47, 49, 54)
    )
    
    embed.add_field(name="💰 Amount", value=f"**₹{amount}**", inline=True)
    embed.add_field(name="📌 Reason", value=f"**{reason}**", inline=True)
    embed.add_field(name="🌐 UPI ID", value="`ankittt.3@fam`", inline=False)
    embed.add_field(name="📲 Payment Mode", value="FamPay / Paytm / PhonePe / Google Pay", inline=False)
    
    embed.set_image(url=QR_IMAGE_URL)
    embed.set_footer(text=FOOTER_TEXT, icon_url=bot.user.display_avatar.url)
    
    await ctx.send(embed=embed)

# ==================== FUN COMMANDS ====================

@bot.command()
async def howgay(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(f"🏳️‍🌈 {member.mention} is **{random.randint(0, 100)}%** Gay!")

@bot.command()
async def cute(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(f"✨ {member.mention} is **{random.randint(0, 100)}%** Cute!")

bot.run(os.getenv('TOKEN'))
      
