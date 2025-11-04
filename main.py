import os
import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from server import keep_alive  # Import keep_alive from server.py
from premium_utils import load_premium, save_premium, add_premium_user, remove_premium_user  # Helper functions for premium

# Run the keep-alive function for Render
keep_alive()  

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
    "https://discord.gg/JgckfuuJg\n"
    "━━━━━━━━━━━━┛"
)

OWNER_ID = 1386627461197987841  # Replace with your Discord user ID

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
        print("✅ Slash commands synced.")
    except Exception as e:
        print(f"Error syncing commands: {e}")

# COMMAND: /a-raid
@bot.tree.command(name="a-raid", description="Spam the main raid message")
async def a_raid(interaction: discord.Interaction):
    await interaction.response.send_message("⚡ Starting raid...", ephemeral=True)
    for _ in range(5):
        await interaction.channel.send(MESSAGE)
        await asyncio.sleep(0.2)

# COMMAND: /custom-raid (Premium Only)
@bot.tree.command(name="custom-raid", description="Send a custom raid message (Premium only)")
async def custom_raid(interaction: discord.Interaction, message: str):
    if interaction.user.id not in load_premium():
        await interaction.response.send_message("💎 Only premium users can use this command.", ephemeral=True)
        return

    await interaction.response.send_message("⚡ Sending custom message...", ephemeral=True)
    for _ in range(5):  # Sends the user-provided message 5 times
        await interaction.channel.send(message)
        await asyncio.sleep(0.2)

# COMMAND: /x-add-premium (Owner Only)
@bot.tree.command(name
