import discord
from discord.ext import commands

def setup_util_commands(bot: commands.Bot):
    @bot.tree.command(name="clean", description="Supprime un certain nombre de messages.")
    async def clean(interaction: discord.Interaction, amount: int = 50):
        """Supprime un nombre de messages spécifié (par défaut 50)."""
        if amount < 1 or amount > 500:
            await interaction.response.send_message("Veuillez entrer un nombre entre 1 et 500.", ephemeral=True)
            return
        
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f"Supprimé {len(deleted)} messages.", ephemeral=True)

        # Gestion des erreurs potentielles
        if len(deleted) == 0:
            await interaction.followup.send("Aucun message à supprimer.", ephemeral=True)
    