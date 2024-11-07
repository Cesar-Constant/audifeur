import json
import random
import time
import discord



async def send_dm_by_uid(ctx, user_id: int, bot):
    # Message prédéfini
    message = "Voici ton message privé"
    rep = False
    try:
        # Récupérer l'utilisateur via son UID
        user = await bot.fetch_user(user_id)

        # Envoyer le message en DM à l'utilisateur
        await user.send(message)

        # Réponse de confirmation dans le chat du serveur
        await ctx.reply(f"Le message a été envoyé en DM à {user}.")

        rep = True
    except discord.Forbidden:
        await ctx.reply(f"Impossible d'envoyer un message en DM à l'utilisateur avec l'UID {user_id}.")
    except discord.NotFound:
        await ctx.reply(f"Impossible de trouver l'utilisateur avec l'UID {user_id}.")
    except discord.HTTPException as e:
        await ctx.reply(f"Une erreur s'est produite lors de l'envoi du message à l'UID {user_id} : {e}")

    return rep

def ravus(ctx, bot):
    # Create the embed message
    embed = discord.Embed(
        title="Qui vas-tu ravusser ma poutrelle ?",
        color=0xFF0000
    )

    # Load the data from the inventory file
    try:
        with open('data/inventory.json', 'r') as f:
            data = json.load(f)
    except Exception as e:
        embed.add_field(name="Erreur", value="Erreur de décodage JSON.", inline=False)
        return {'embed': embed}

    # Search for the user's inventory
    found_item = False
    for obj in data:
        if obj.get('userId') == ctx.author.id:
            if obj.get('objects'):

                for item in obj['objects']:
                    if item.get('obj') == 7:
                        dest = data[random.randint(0, len(data))].get('userId')
                        while not send_dm_by_uid(ctx,dest, bot):
                            dest = data[random.randint(0, len(data))].get('userId')

                        found_item = True
                        embed.add_field(name="Description", value="RAAAAVUUUUUUUUS", inline=False)
                        break  # Exit loop once found
            break  # Exit outer loop once the user's inventory is processed

    if not found_item:
        embed.add_field(name="Description", value="Tu n'as pas l'âme de la poutrelle.", inline=False)

    return {'embed': embed}