import json
import os
import random
import time
from classes.objects.Mutition import Munition
from classes.objects.Feur import Feur
from classes.objects.Caillou import Caillou
from classes.Bot import Bot

class User:

  @staticmethod
  async def kick(userId, bot):
    member = User.findUser(bot, userId)
    await member.kick(reason="Connard")

  @staticmethod
  async def generateInventory(bot):
    members = User.findUsers(bot)

    user_data = []
    for member in members:
      user_data.append({"userId": member.id, "objects": []})

    file_path = "data/inventory.json"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as f:
      json.dump(user_data, f, indent=4)

  @staticmethod
  def findUsers(bot):
      guild = bot.guilds[0]
      return guild.members

  @staticmethod
  def findUser(bot, userId):
    guild = bot.guilds[0]
    return guild.get_member(userId)

  @staticmethod
  def decrementQuantity(userId, itemId):
    with open('data/inventory.json', 'r') as f:
      data = json.load(f)
      done = False

    for user in data:
      if user["userId"] == int(userId):
        for obj in user['objects']:
          if obj['obj'] == int(itemId):
            if obj['quantity'] == 1:
              user['objects'].remove(obj)
            else:
              obj['quantity'] -= 1

            done = True

    with open('data/inventory.json', 'w') as f:
      json.dump(data, f, indent=2)

    return done

  @staticmethod
  async def useItem(ctx, bot):
    if len(ctx.message.content.split(' ')) > 3:
      return Bot.showError('Oups clodo !', "Connard apprend à écrire !")

    userId = ctx.author.id
    itemId = ctx.message.content.split(' ')[1]

    if not (User.decrementQuantity(userId, itemId)):
      return Bot.showError('Oups clodo !', "Connard obtiens le !")

    if itemId == '3':
      try:
        enemy = ctx.message.content.split(' ')[2][2:len(ctx.message.content.split(' ')[2]) - 1]
      except():
        return Bot.showError('Oups clodo !', "Tu as oublié de viser qqn")

      return await Caillou.use(enemy)

    elif itemId == '4':
      return await Feur.use()
    elif itemId == '6':
      return await Munition.use()

  @staticmethod
  def addToInventory(obj, userId):
    add = True
    with open('data/inventory.json', 'r') as f:
      data = json.load(f)

    for user in data:
      if user['userId'] == userId:
        for i in range(len(user["objects"])):
          if obj['id'] == user["objects"][i]['obj']:
            user["objects"][i]['quantity'] += 1
            add = False

        if add:
          user['objects'].append({
            "obj": obj['id'],
            "date": int(time.time()),
            "quantity": 1
          })

        break

    with open('data/inventory.json', 'w') as f:
      json.dump(data, f, indent=2)

    return Bot.showItem(obj)

  @staticmethod
  def loot(userId):
    with open('data/inventory.json', 'r') as f:
      data = json.load(f)
      for user in data:
        if user["userId"] == userId and user["objects"] != [] and int(time.time()) - \
                user["objects"][len(user["objects"]) - 1]["date"] < 1800:
          return Bot.showError('Attends !',
                           "Tu ne peux fouiller les poubelles qu'une fois toutes les 30 minutes sale clochard !")

    with open('data/objects.json', 'r') as f:
      objects = json.load(f)

    weights = []

    for obj in objects:
      weights.append(obj["chance"])

    x = random.choices(objects, weights=weights)
    return User.addToInventory(x[0], userId)