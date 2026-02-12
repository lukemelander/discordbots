# ComBot - Discord Bot

A Discord bot for OTC stock alerts, FinViz screener data, and fun commands.

## Features

- **OTC Alerts**: Monitors FINRA OTC daily list for new additions
- **Stock Screener**: Get insider trading info, news, and price targets from FinViz
- **OpenSea Integration**: Check NFT collection floor prices and stats
- **Fun Commands**: Futurama quotes, Portal quotes, cat/dog pictures, and more

## Commands

- `CB help` - Shows all commands
- `CB cat` - Random cat picture
- `CB dog` - Random dog picture
- `CB catfact` - Random cat fact
- `CB N [TICKER]` - News for a stock
- `CB I [TICKER]` - Insider trading info
- `CB PT [TICKER]` - Price targets
- `CB F [collection]` - OpenSea floor price

## Trigger Phrases

- `FUTURAMA` - Random Futurama quote
- `PORTAL` - Random GLaDOS quote
- `SKYNET` - "I am inevitable"
- `ASIMOV` - The three laws of robotics
- `SAY HELLO` - Friendly greeting
- `COMBOT IS BACK` - "News of my demise was greatly exaggerated"

## Setup

1. Create a Discord bot at https://discord.com/developers/applications
2. Copy your bot token
3. Edit `.env` file with your token and channel ID
4. Upload to your hosting provider
5. Set `OTCbot.py` as the startup file

## Files

- `OTCbot.py` - Main bot file
- `quotes_holder.py` - Quote collections
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (keep private!)
- `cogs/` - Command modules
  - `maincog.py` - Fun responses
  - `screener.py` - FinViz commands
  - `opensea.py` - NFT commands
  - `animals.py` - Cat/dog pictures
- `images/` - Image files for responses
