import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from flask import Flask
from threading import Thread

# Web server for Replit 24/7
app = Flask('')

@app.route('/')
def home():
    return "Hare Krishna! Bot is alive."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Set up intents
intents = discord.Intents.default()
intents.message_content = True

# Create bot
bot = commands.Bot(command_prefix='!', intents=intents)

# On bot ready
@bot.event
async def on_ready():
    print(f'✅ Bot is ready. Logged in as {bot.user}')

# Test command
@bot.command()
async def test(ctx):
    await ctx.send("Hare Krishna! Bot is alive and responding!")

# Merged verse logic for all scriptures
merged_verses = {
    'bg': {
        1: [(16, 18), (21, 22), (32, 35), (37, 38)],
        2: [(42, 43)],
        5: [(8, 9), (27, 28)],
        6: [(11, 12), (13, 14), (20, 23)],
        10: [(4, 5), (12, 13)],
        11: [(10, 11), (26, 27), (41, 42)],
        12: [(3, 4), (6, 7), (13, 14), (18, 19)],
        13: [(1, 2), (6, 7), (8, 12)],
        14: [(22, 25)],
        15: [(3, 4)],
        16: [(1, 3), (11, 12), (13, 15)],
        17: [(5, 6), (26, 27)],
        18: [(51, 53)]
    },
    'sb': {},  # You can add merged verse logic here for SB if needed
    'cc': {}   # You can add merged verse logic here for CC if needed
}

def resolve_url(scripture, chapter, verse):
    if scripture in merged_verses and chapter in merged_verses[scripture]:
        for start, end in merged_verses[scripture][chapter]:
            if start <= verse <= end:
                return f"https://vedabase.io/en/library/{scripture}/{chapter}/{start}-{end}/"
    return f"https://vedabase.io/en/library/{scripture}/{chapter}/{verse}/"

# Scrape Vedabase verse

def scrape_vedabase_verse(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        devanagari = soup.find('h2', string='Devanagari')
        devanagari = devanagari.find_next('div').text.strip() if devanagari else ""

        verse_text = soup.find('h2', string='Verse text')
        verse_text = verse_text.find_next('div').text.strip() if verse_text else ""

        translation = soup.find('h2', string='Translation')
        translation = translation.find_next('div').text.strip() if translation else ""

        purport = soup.find('h2', string='Purport')
        purport = purport.find_next('div').text.strip() if purport else ""

        synonyms = soup.find('h2', string='Synonyms')
        synonyms = synonyms.find_next('div').text.strip() if synonyms else ""

        return {
            'devanagari': devanagari,
            'verse_text': verse_text,
            'translation': translation,
            'purport': purport,
            'synonyms': synonyms
        }
    except requests.RequestException as e:
        return f"Error fetching the webpage: {e}"
    except AttributeError as e:
        return f"Error parsing the content: {e}"

# Send verse as an embed
async def send_verse_embed(ctx, scripture_name, verse_number, content, color):
    if isinstance(content, dict):
        embed = discord.Embed(title=f"{scripture_name} {verse_number}", color=color)

        for label, text in content.items():
            if text:
                for i in range(0, len(text), 1024):
                    embed.add_field(
                        name=label.capitalize() if i == 0 else f"{label.capitalize()} (cont'd)",
                        value=text[i:i+1024],
                        inline=False
                    )

        await ctx.send(embed=embed)
    else:
        await ctx.send(content)

# Bhagavad Gita command
@bot.command(name='bg')
async def fetch_bg_verse(ctx, verse_number: str):
    try:
        chapter, verse = map(int, verse_number.split("."))
        url = resolve_url("bg", chapter, verse)
        verse_content = scrape_vedabase_verse(url)
        await send_verse_embed(ctx, "Bhagavad Gita", verse_number, verse_content, discord.Color.purple())
    except:
        await ctx.send("Please enter a valid verse format like 2.13")

# Srimad Bhagavatam command
@bot.command(name='sb')
async def fetch_sb_verse(ctx, verse_number: str):
    try:
        chapter, verse = map(int, verse_number.split("."))
        url = resolve_url("sb", chapter, verse)
        verse_content = scrape_vedabase_verse(url)
        await send_verse_embed(ctx, "Srimad Bhagavatam", verse_number, verse_content, discord.Color.blue())
    except:
        await ctx.send("Please enter a valid verse format like 1.1")

# Chaitanya Charitamrita command
@bot.command(name='cc')
async def fetch_cc_verse(ctx, verse_number: str):
    try:
        chapter, verse = map(int, verse_number.split("."))
        url = resolve_url("cc", chapter, verse)
        verse_content = scrape_vedabase_verse(url)
        await send_verse_embed(ctx, "Chaitanya Charitamrita", verse_number, verse_content, discord.Color.green())
    except:
        await ctx.send("Please enter a valid verse format like 2.13")

# Keep bot alive on Replit
keep_alive()

# Run your bot (Replace with your actual bot token)
bot.run("YOUR_DISCORD_BOT_TOKEN")

