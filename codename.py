import discord
from discord.ext import commands
import random

def setup_codename_commands(bot: commands.Bot):
    @bot.tree.command(name='codename', description='Démarre ou arrête une partie de Codenames.')
    async def codename(interaction: discord.Interaction, action: str, code: str = None):
        """Démarre ou arrête une partie de Codenames."""
        print(f"Commande /codename exécutée avec action: {action}, code: {code}")  # Log de débogage
        if action == "start" and code:
            await start_codename(interaction, code)
        elif action == "stop":
            await stop_codename(interaction)
        else:
            await interaction.response.send_message(
                "Utilisation : /codename start <code> ou /codename stop.",
                ephemeral=True
            )

    async def start_codename(interaction: discord.Interaction, code: str):
        """Démarre une partie de Codenames."""
        print(f"Démarrage de la partie Codenames avec le code: {code}")  # Log de débogage
        guild = interaction.guild
        category = interaction.channel.category

        try:
            # Créer les canaux
            spymaster_channel = await guild.create_voice_channel("Spymaster", category=category)
            operators_channel = await guild.create_voice_channel("Operators", category=category)
            text_channel = await guild.create_text_channel(f"codename-{code}", category=category)

            # Déplacer les membres
            codename_channel = interaction.channel
            members = codename_channel.members

            if len(members) < 2:
                await interaction.response.send_message(
                    "Pas assez de membres dans le canal pour démarrer la partie.",
                    ephemeral=True
                )
                return

            random_members = random.sample(members, min(2, len(members)))

            for member in random_members:
                await member.move_to(spymaster_channel)

            for member in members:
                if member not in random_members:
                    await member.move_to(operators_channel)

            game_url = f"https://codename.fr/{code}"
            await text_channel.send(f"Voici l'URL de la partie : {game_url}")

            await interaction.response.send_message(
                f"La partie Codenames a démarré ! Canaux créés : {spymaster_channel.mention}, {operators_channel.mention}, {text_channel.mention}",
                ephemeral=True
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "Je n'ai pas les permissions nécessaires pour créer des canaux.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"Désolé, une erreur est survenue lors de la création des canaux : {str(e)}",
                ephemeral=True
            )

    async def stop_codename(interaction: discord.Interaction):
        """Arrête une partie de Codenames."""
        print("Arrêt de la partie Codenames")  # Log de débogage
        guild = interaction.guild

        try:
            spymaster_channel = discord.utils.get(guild.voice_channels, name="Spymaster")
            operators_channel = discord.utils.get(guild.voice_channels, name="Operators")
            text_channel = discord.utils.get(guild.text_channels, name=lambda name: name.startswith("codename-"))

            if spymaster_channel:
                for member in spymaster_channel.members:
                    await member.move_to(None)  # Les renvoie au canal par défaut

            if operators_channel:
                for member in operators_channel.members:
                    await member.move_to(None)  # Les renvoie au canal par défaut

            # Suppression des canaux
            if spymaster_channel:
                await spymaster_channel.delete()
            if operators_channel:
                await operators_channel.delete()
            if text_channel:
                await text_channel.delete()

            await interaction.response.send_message(
                "La partie Codenames a été arrêtée et les canaux ont été supprimés.",
                ephemeral=False
            )
        except Exception as e:
            await interaction.response.send_message(
                f"Désolé, une erreur est survenue lors de l'arrêt de la partie : {str(e)}",
                ephemeral=False
            )
