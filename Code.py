import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from flask import Flask
from threading import Thread

# --- Flask Web Server to Keep Bot Alive (Replit + UptimeRobot) ---
app = Flask('')

@app.route('/')
def home():
    return "Hare Krishna! Bot is alive."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- Discord Bot Setup ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot is ready. Logged in as {bot.user}')

@bot.command()
async def test(ctx):
    await ctx.send("Hare Krishna! Bot is alive and responding!")

# --- Scraper Function ---
def scrape_vedabase_verse(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        devanagari = soup.find('h2', string='Devanagari').find_next('div').text.strip()
        verse_text = soup.find('h2', string='Verse text').find_next('div').text.strip()
        translation = soup.find('h
