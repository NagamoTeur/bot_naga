import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
print(f"Token chargé : {token}")  # Pour le débogage

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Importer les commandes
from isaac import setup_isaac_commands
from codename import setup_codename_commands

# Configurer les commandes
setup_isaac_commands(bot)
setup_codename_commands(bot)

@bot.event
async def on_ready():
    print(f'Nous sommes connectés en tant que {bot.user}')
    await bot.tree.sync()  # Synchroniser les commandes
    print("Commandes synchronisées avec succès.")  # Message de confirmation

# Lancer le bot
bot.run(token)