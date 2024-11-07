import discord
import random
from discord import Object

class Caillou(Object):

  id = 1,
  name = "Peste noire",
  description = "Purge kick tous les gens du serv, sauf les admins.",
  chance = 0.01,
  url = "images/plague.jpg"

  @staticmethod
  async def use(enemy):
    if random.randint(0, 1) == 0:
      embed = discord.Embed(
        title="Il prend son élan et ...",
        description=f"Rate son tire comme une merde",
        color=0xFF0000,
      )
    else:
      embed = discord.Embed(
        title="Il prend son élan et ...",
        description=f"Envoie un parpaing dans la gueule de <@{enemy}>",
        color=0xFF0000,
      )

    return {'embed': embed}