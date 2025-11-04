import os
import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from server import keep_alive  # Keeps the bot alive on Render
from premium_utils import load_premium, save_premium, add_premium_user, remove_premium_user  # Premium utilities

# Run the keep_alive function (used for Render hosting)
keep_alive()

# RAID Message Content
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
    "https://discord.gg/JgckfuuJg\n"
    "━━━━━━━━━━━━┛"
)

# Set the OWNER ID (Replace this with your Discord user ID)
OWNER_ID = 1386627461197987841

# Initialize the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")
    try:
        await bot.tree.sync()  # Sync slash commands with Discord
        print("✅ Slash commands synced successfully.")
    except Exception as e:
        print(f"Error syncing commands: {e}")

# COMMAND: /a-raid (Spam the main message)
@bot.tree.command(name="a-raid", description="Spam the main raid message")
async def a_raid(interaction: discord.Interaction):
    await interaction.response.send_message("⚡ Starting raid...", ephemeral=True)
    for _ in range(5):  # Sends message 5 times
        await interaction.channel.send(MESSAGE)
        await asyncio.sleep(0.2)

# COMMAND: /custom-raid (For Premium Users Only)
@bot.tree.command(name="custom-raid", description="Send a custom raid message (Premium only)")
async def custom_raid(interaction: discord.Interaction, message: str):
    if interaction.user.id not in load_premium():  # Check if user is in premium list
        await interaction.response.send_message("💎 Only premium users can use this command.", ephemeral=True)
        return
    await interaction.response.send_message("⚡ Sending custom message...", ephemeral=True)
    for _ in range(5):
        await interaction.channel.send(message)
        await asyncio.sleep(0.2)

# COMMAND: /x-add-premium (Owner Only Command to Add Premium User)
@bot.tree.command(name="x-add-premium", description="Add a user to premium users")
@app_commands.describe(user="The user to add to premium")
async def add_premium(interaction: discord.Interaction, user: discord.User):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("❌ You don’t have permission to perform this action.", ephemeral=True)
        return
    add_premium_user(user.id)
    await interaction.response.send_message(f"✅ {user.mention} added to premium users.", ephemeral=True)

# COMMAND: /x-remove-premium (Owner Only Command to Remove Premium User)
@bot.tree.command(name="x-remove-premium", description="Remove a user from premium users")
@app_commands.describe(user="The user to remove from premium")
async def remove_premium(interaction: discord.Interaction, user: discord.User):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("❌ You don’t have permission to perform this action.", ephemeral=True)
        return
    if remove_premium_user(user.id):
        await interaction.response.send_message(f"✅ {user.mention} removed from premium users.", ephemeral=True)
    else:
        await interaction.response.send_message(f"⚠️ {user.mention} is not in the premium list.", ephemeral=True)

# Run the bot using the token from Render's environment variables
bot.run(os.getenv("DISCORD_TOKEN"))
