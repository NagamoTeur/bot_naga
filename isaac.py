import discord
from discord.ext import commands
import random

def setup_isaac_commands(bot: commands.Bot):
    @bot.tree.command(name='isaac', description='Génère un défi Isaac aléatoire.')
    async def isaac(interaction: discord.Interaction, nombre_regles: int = 2):
        """Génère un défi Isaac aléatoire avec un nombre de règles spécifié (par défaut 2)."""
        objectifs = [
            "Mom", "Mom's heart", "The Lamb", "Satan", "Mega Satan", 
            "Delirium", "Mother", "The Beast", "Boss Rush", "Isaac", "Blue Baby"
        ]
        personnages = [
            "Isaac", "Magdalene", "Cain", "Judas", "Eve", "Samson", 
            "Azazel", "Lazarus", "Eden", "The Lost", "Lilith", 
            "Apollyon", "Forgotten", "Bethany", "Jacob & Esau", "Keeper"
        ]
        regles_difficulte = [
            "Pas de Devil Deals", "Pas de trinkets", "Pas de clé", "Pas de bombes", 
            "Interdit de ramasser des pièces", "Seul les objets du stage 1", 
            "Transformations interdites", "Moins de 10 objets", 
            "Explorer toutes les pièces de chaque étage", 
            "Pas d'angel room (sauf si mega satan)", 
            "1 seul coeur à partir du deuxième étage"
        ]

        try:
            nombre_regles = min(max(nombre_regles, 0), len(regles_difficulte))
            objectif = random.choice(objectifs)
            personnage = random.choice(personnages)
            regles = random.sample(regles_difficulte, nombre_regles) if nombre_regles > 0 else []

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
