import discord
from discord import Object

class Feur(Object):

  id = 4,
  name = "FEUR",
  description = "Sert à rien, juste à rien.",
  chance = 30,
  url = "images/monalisa.png"

  @staticmethod
  async def use(enemy=''):
    embed = discord.Embed(
      title='QUOI ?',
      description=f"FEUR FEUR FEUR",
      color=0xFF0000,
    )

    return {'embed': embed}