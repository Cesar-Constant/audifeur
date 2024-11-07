import discord
from discord import Object

class Munition(Object):

  id = 6
  name = "Mutition.py"
  description ="Nécessaire à l'utilisation du glock."
  chance = 10
  url = "images/ammo.png"

  @staticmethod
  async def use(enemy=''):
    embed = discord.Embed(
      title="Bien joué ! ",
      description=f"Tu as lancé la balle, mais t'as oublie de la mettre dans un glock...",
      color=0xFF0000,
    )

    return {'embed': embed}