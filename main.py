import os
import json
import asyncio
from colorama import Fore, init
import discord
from discord.ext import commands
from discord import app_commands
from server import keep_alive  # aici apelăm serverul fără circular import

init(autoreset=True)

# --- START SERVER ---
keep_alive()
# -------------------

PREMIUM_FILE = "premium.json"

def load_premium_users():
    if not os.path.exists(PREMIUM_FILE):
        return []
    with open(PREMIUM_FILE, "r") as f:
        return json.load(f)

def save_premium_users(user_ids):
    with open(PREMIUM_FILE, "w") as f:
        json.dump(user_ids, f, indent=2)

def add_premium_user(user_id: int):
    premium_users = load_premium_users()
    if user_id not in premium_users:
        premium_users.append(user_id)
        save_premium_users(premium_users)

def remove_premium_user(user_id: int) -> bool:
    premium_users = load_premium_users()
    if user_id in premium_users:
        premium_users.remove(user_id)
        save_premium_users(premium_users)
        return True
    return False

# Mesaj de raid
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
    "@everyone"
)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

OWNER_ID = 1386627461197987841

@bot.event
async def on_ready():
    print(f"{Fore.CYAN}Logged in as {bot.user}{Fore.RESET}")
    try:
        synced = await bot.tree.sync()
        print(f"{Fore.CYAN}Synced {len(synced)} commands.")
    except Exception as e:
        print(f"Could not sync commands: {e}")

# Comenzi bot
@bot.tree.command(name="a-raid", description="Spam a special guild raid message.")
async def araid(interaction: discord.Interaction):
    await interaction.response.send_message("Raiding now...", ephemeral=True)
    for _ in range(5):
        await asyncio.sleep(0.2)
        await interaction.followup.send(MESSAGE)

@bot.tree.command(name="custom-raid", description="Premium Raid with your own message. (premium only!)")
@app_commands.describe(message="Your custom message to spam")
async def custom_raid(interaction: discord.Interaction, message: str = None):
    premium_users = load_premium_users()
    if interaction.user.id not in premium_users:
        await interaction.response.send_message("💎 This command is only for premium users.", ephemeral=True)
        return
    spam_message = message if message else "Custom Raid!"
    await interaction.response.send_message(f"💎 SPAM TEXT:\n```{spam_message}```", ephemeral=True)
    for _ in range(5):
        await asyncio.sleep(0.2)
        await interaction.followup.send(spam_message)

@bot.tree.command(name="x-add-premium", description="Grant premium access to a user. (owner only)")
@app_commands.describe(user="The user to grant premium access to")
async def add_premium(interaction: discord.Interaction, user: discord.User):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
        return
    add_premium_user(user.id)
    await interaction.response.send_message(f"✅ {user.mention} is now premium!", ephemeral=True)

@bot.tree.command(name="x-rem-premium", description="Remove premium access from a user. (owner only)")
@app_commands.describe(user="The user to remove premium access from")
async def rem_premium(interaction: discord.Interaction, user: discord.User):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
        return
    removed = remove_premium_user(user.id)
    if removed:
        await interaction.response.send_message(f"✅ {user.mention} removed from premium!", ephemeral=True)
    else:
        await interaction.response.send_message(f"⚠️ {user.mention} was not premium.", ephemeral=True)

if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    if TOKEN:
        bot.run(TOKEN)
    else:
        print(Fore.RED + "❌ Error: Unable to load bot token (set as DISCORD_TOKEN env variable).")
