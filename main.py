import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import random

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
print(f"Token chargé : {token}")  # Ajoute cette ligne pour déboguer

client = discord.Client(intents=discord.Intents.all())

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

@client.event
async def on_ready():
    print(f'Nous sommes connectés en tant que {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/isaac'):
        args = message.content.split()
        nombre_regles = 2  # Valeur par défaut

        if len(args) > 1 and args[1].isdigit():
            nombre_regles = min(max(int(args[1]), 0), len(regles_difficulte))  # Limiter le nombre de règles

        objectif = random.choice(objectifs)
        personnage = random.choice(personnages)
        regles = random.sample(regles_difficulte, nombre_regles) if nombre_regles > 0 else []

        # Stocker les informations de run
        run_data[message.author.id] = {
            'personnage': personnage,
            'objectif': objectif,
            'regles': regles
        }

        await message.channel.send(
            f"{message.author.mention}, voici ton défi Isaac : \n"
            f"* Joue avec **{personnage}** \n"
            f"* Objectif : **{objectif}** \n"
            f"* Règles : {', '.join(regles) if regles else 'Aucune règle imposée.'}"
        )

    elif message.content.startswith('/reroll'):
        if message.author.id in run_data:
            # Récupérer les informations de run précédentes
            personnage = run_data[message.author.id]['personnage']
            objectif = run_data[message.author.id]['objectif']
            nombre_regles = 2  # On peut choisir toutes les règles

            # Reroll des règles
            new_regles = random.sample(regles_difficulte, nombre_regles) if nombre_regles > 0 else []

            run_data[message.author.id]['regles'] = new_regles

            await message.channel.send(
                f"{message.author.mention}, voici les nouvelles règles pour ton défi Isaac : \n"
                f"* Joue avec **{personnage}** \n"
                f"* Objectif : **{objectif}** \n"
                f"* Nouvelles règles : {', '.join(new_regles) if new_regles else 'Aucune règle imposée.'}"
            )
        else:
            await message.channel.send(f"{message.author.mention}, tu n'as pas encore lancé de défi. Utilise `/isaac` d'abord.")

client.run(token=token)
