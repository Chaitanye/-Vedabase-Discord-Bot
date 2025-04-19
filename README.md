
# 📖 Vedabase Discord Bot

A Discord bot that fetches and displays verses from the **Bhagavad Gita**, **Śrīmad Bhāgavatam**, and **Chaitanya Charitāmṛta** directly from [Vedabase.io](https://vedabase.io/).  
Built using Python, BeautifulSoup, Discord.py, and Flask (for 24/7 uptime via UptimeRobot + Replit).

---

## ✨ Features

- 🔍 Fetch verses using commands:
  - `!bg 4.7` → Bhagavad Gita 4.7
  - `!sb 1.1.1` → Śrīmad Bhāgavatam 1.1.1
  - `!cc adi.1.1` → Chaitanya Charitāmṛta Ādi-līlā 1.1
- 📜 Returns:
  - Devanagari
  - Synonyms
  - Verse (IAST Roman transliteration)
  - Translation
  - Purport
- 🖼️ Uses Discord embeds for clean and readable formatting
- 🌐 Keeps bot online 24/7 using Flask + UptimeRobot on Replit
- 🙏 Simple `!test` command to confirm bot is alive

---

## 🚀 How it works

- The bot scrapes data from Vedabase using `requests` and `BeautifulSoup`.
- All content is structured into a Discord embed and returned when a user sends a valid command.
- A small Flask web server is included to keep the bot alive on Replit via UptimeRobot pings.

---

## 🔧 Tech Stack

- Python 3
- [discord.py](https://github.com/Rapptz/discord.py)
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)
- Flask (for uptime ping)
- Replit (hosting)
- UptimeRobot (pings to keep the project awake)

---

## 🛠️ Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
