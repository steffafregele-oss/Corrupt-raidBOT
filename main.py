from server import keep_alive
import os
import json
import asyncio
import discord
from discord.ext import commands
from discord import app_commands

# PORNIM SERVERUL (pentru Render/UptimeRobot)
keep_alive()

# PREMIUM DATABASE
PREMIUM_FILE = "premium.json"

def load_premium():
    if not os.path.exists(PREMIUM_FILE):
        return []
    return json.load(open(PREMIUM_FILE))

def save_premium(data):
    json.dump(data, open(PREMIUM_FILE, "w"), indent=2)

def add_premium_user(user_id):
    users = load_premium()
    if user_id not in users:
        users.append(user_id)
        save_premium(users)

def remove_premium_user(user_id):
    users = load_premium()
    if user_id in users:
        users.remove(user_id)
        save_premium(users)
        return True
    return False

# RAID MESSAGE
MESSAGE = (
    "**- 🦴 3 OP GENERATORS,\n"
    "- 🌐 HAVE OWN SITE,\n"
    "- 🧠 OP METHODS,\n"
    "- 👀 !STATS BOT\n"
    "- 🫆 MANAGE UR OWN SITE/DASHBOARD,\n"
    "- 🗒️ USERNAME & PASSWORD,\n"
    "- 🔒 ACCOUNT STATUS,\n"
    "- 🚀 FAST LOGIN SPEED\n"
    "- 📷 FULL TUTORIALS ON HOW TO BEAM**\n"
    "━━━━━━━━━━━━┓\n"
    " https://discord.gg/JgckfuuJg\n"
    "━━━━━━━━━━━━┛\n"
)

# BOT CONFIG
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

OWNER_ID = 1386627461197987841  # ← ID-ul tău

# READY EVENT
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        await bot.tree.sync()
        print("✅ Slash commands synced.")
    except:
        pass

# RAID COMMAND
@bot.tree.command(name="a-raid", description="Spam the main raid message")
async def a_raid(interaction: discord.Interaction):
    await interaction.response.send_message("⚡ Starting raid...", ephemeral=True)
    for _ in range(5):
        await interaction.channel.send(MESSAGE)
        await asyncio.sleep(0.2)

# PREMIUM CUSTOM RAID DM
@bot.tree.command(name="custom-raid", description="Send a DM using premium")
@app_commands.describe(user="User to DM", message="Message to send")
async def custom_raid(interaction: discord.Interaction, user: discord.User, message: str):
    if interaction.user.id not in load_premium():
        await interaction.response.send_message("💎 Only premium users can use this command.", ephemeral=True)
        return

    try:
        await user.send(message)
        await interaction.response.send_message(f"✅ Sent to {user.mention}", ephemeral=True)
    except:
        await interaction.response.send_message("❌ Cannot DM this user.", ephemeral=True)

# ADD PREMIUM (OWNER ONLY)
@bot.tree.command(name="x-add-premium", description="Give someone premium")
@app_commands.describe(user="User to add")
async def add_premium_cmd(interaction: discord.Interaction, user: discord.User):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("❌ Not allowed.", ephemeral=True)
        return
    add_premium_user(user.id)
    await interaction.response.send_message(f"✅ {user.mention} now has premium!", ephemeral=True)

# REMOVE PREMIUM (OWNER ONLY)
@bot.tree.command(name="x-rem-premium", description="Remove premium access")
@app_commands.describe(user="User to remove")
async def remove_premium_cmd(interaction: discord.Interaction, user: discord.User):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("❌ Not allowed.", ephemeral=True)
        return
    if remove_premium_user(user.id):
        await interaction.response.send_message(f"✅ Removed premium from {user.mention}", ephemeral=True)
    else:
        await interaction.response.send_message("⚠️ User was not premium.", ephemeral=True)

# RUN BOT
bot.run(os.getenv("DISCORD_TOKEN"))
