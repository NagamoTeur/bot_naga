import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import random

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
print(f"Token chargé : {token}")  # Pour le débogage

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Listes pour stocker les objectifs, personnages et règles
objectifs = [
    "Mom",
    "Mom's heart",
    "The Lamb",
    "Satan",
    "Mega Satan",
    "Delirium",
    "Mother",
    "The Beast",
    "Boss Rush",
    "Isaac",
    "Blue Baby"
]
personnages = [
    "Isaac",
    "Magdalene",
    "Cain",
    "Judas",
    "Eve",
    "Samson",
    "Azazel",
    "Lazarus",
    "Eden",
    "The Lost",
    "Lilith",
    "Apollyon",
    "Forgotten",
    "Bethany",
    "Jacob & Esau",
    "Keeper"
]
regles_difficulte = [
    "Pas de Devil Deals",
    "Pas de trinkets",
    "Pas de clé",
    "Pas de bombes",
    "Interdit de ramasser des pièces",
    "Seul les objets du stage 1",
    "Transformations interdites",
    "Moins de 10 objets",
    "Explorer toutes les pièces de chaque étage",
    "Pas d'angel room (sauf si mega satan)",
    "1 seul coeur à partir du deuxième étage"
]

# Dictionnaire pour stocker les informations de run
run_data = {}

@bot.tree.command(name='isaac', description='Génère un défi Isaac aléatoire.')
async def isaac(interaction: discord.Interaction, nombre_regles: int = 2):
    """Génère un défi Isaac aléatoire avec un nombre de règles spécifié (par défaut 2)."""
    try:
        nombre_regles = min(max(nombre_regles, 0), len(regles_difficulte))  # Limiter le nombre de règles

        objectif = random.choice(objectifs)
        personnage = random.choice(personnages)
        regles = random.sample(regles_difficulte, nombre_regles) if nombre_regles > 0 else []

        # Stocker les informations de run
        run_data[interaction.user.id] = {
            'personnage': personnage,
            'objectif': objectif,
            'regles': regles
        }

        await interaction.response.send_message(
            f"{interaction.user.mention}, voici ton défi Isaac : \n"
            f"* Joue avec **{personnage}** \n"
            f"* Objectif : **{objectif}** \n"
            f"* Règles : {', '.join(regles) if regles else 'Aucune règle imposée.'}"
        )
    except Exception as e:
        await interaction.response.send_message(
            f"Désolé {interaction.user.mention}, une erreur est survenue : {str(e)}"
        )
        print(f"Erreur lors de la génération du défi : {e}")

@bot.tree.command(name='clean', description='Supprime un certain nombre de messages du canal actuel.')
async def clean(interaction: discord.Interaction, nombre_messages: int = 50):
    """Supprime un nombre spécifié de messages du canal actuel."""
    try:
        channel = interaction.channel
        
        # Limiter le nombre de messages à 100 maximum et à 1 minimum
        nombre_messages = min(max(nombre_messages, 1), 100)

        deleted = await channel.purge(limit=nombre_messages)  # Supprime le nombre de messages spécifié
        await interaction.response.send_message(f"{len(deleted)} messages supprimés.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(
            f"Désolé, une erreur est survenue lors de la suppression des messages : {str(e)}"
        )
        print(f"Erreur lors de la suppression des messages : {e}")

@bot.event
async def on_ready():
    print(f'Nous sommes connectés en tant que {bot.user}')
    await bot.tree.sync()  # Synchroniser les commandes
    print("Commandes synchronisées avec succès.")  # Message de confirmation

bot.run(token)
