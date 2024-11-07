import os
import json
import random
import time
import discord

async def generateInventory(bot):
    members = findUsers(bot)

    user_data = []
    for member in members:
        user_data.append({"userId": member.id, "objects": []})

    file_path = "data/inventory.json"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as f:
        json.dump(user_data, f, indent=4)

def loot(userId):
    with open('data/inventory.json', 'r') as f:
        data = json.load(f)
        for user in data:
            if user["userId"] == userId and user["objects"] != [] and int(time.time()) - user["objects"][len(user["objects"]) - 1]["date"] < 1800:
                return showError('Attends !', "Tu ne peux fouiller les poubelles qu'une fois toutes les 30 minutes sale clochard !")

    with open('data/objects.json', 'r') as f:
        objects = json.load(f)

    weights = []

    for obj in objects:
        weights.append(obj["chance"])

    x = random.choices(objects, weights=weights)
    return addToInventory(x[0], userId)

def addToInventory(obj, userId):
    add = True
    with open('data/inventory.json', 'r') as f:
        data = json.load(f)

    for utilisateur in data:
        if utilisateur['userId'] == userId:
            for i in range(len(utilisateur["objects"])):
                if obj['id'] == utilisateur["objects"][i]['obj']:
                    utilisateur["objects"][i]['quantity'] += 1
                    add = False

            if(add):
                utilisateur['objects'].append({
                    "obj": obj['id'],
                    "date": int(time.time()),
                    "quantity": 1
                })

            break

    with open('data/inventory.json', 'w') as f:
        json.dump(data, f, indent=2)

    return showItem(obj)

def showItem(obj):
    embed = discord.Embed(
        title=obj['name'],
        description=obj['description'],
        color=0xFF0000,
    )

    file = discord.File(obj["url"], filename="image.png")
    embed.set_image(url="attachment://image.png")

    return {'embed': embed, 'file': file}

def showError(title, message):
    embed = discord.Embed(
        title=title,
        description=message,
        color=0xFF0000,
    )

    file = discord.File('images/middleFinger.png', filename="image.png")
    embed.set_image(url="attachment://image.png")

    return {'embed': embed, 'file': file}

def showInventory(userId):
    embed = discord.Embed(
        title="Qu'est ce qu'il y a dans tes poches ?",
        color=0xFF0000,
    )

    objects = []

    with open('data/inventory.json', 'r') as f:
        data = json.load(f)
        for user in data:
            if user["userId"] == userId:
                objects = user["objects"]

    if(len(objects) == 0):
        embed.add_field(name='Rien', value="Y'a rien dans tes poches connard !", inline=False)

    else:
        with open('data/objects.json', 'r') as f:
            data = json.load(f)
            for o in objects:
                for obj in data:
                    if(obj['id'] == o["obj"]):
                        title = f"[{obj['id']}] {obj['name']} X {o['quantity']}"
                        embed.add_field(name=title , value=obj['description'], inline=False)
    return embed

def findUsers(bot):
    guild = bot.guilds[0]
    return guild.members

def findUser(bot, userId):
    guild = bot.guilds[0]
    return guild.get_member(userId)

async def useItem(ctx, bot):
    if(len(ctx.message.content.split(' ')) > 3):
        return showError('Oups clodo !', "Connard apprend à écrire !")

    userId = ctx.author.id
    itemId = ctx.message.content.split(' ')[1]

    if not (decrementeQuantity(userId, itemId)):
        return showError('Oups clodo !', "Connard obtiens le !")

    if(itemId == '3'):
        try:
            enemy = ctx.message.content.split(' ')[2][2:len(ctx.message.content.split(' ')[2]) - 1]
        except():
            return showError('Oups clodo !', "Tu as oublié de viser qqn")

        return await throwRock(enemy, ctx)
    elif(itemId == '2'):
        return await explosiveBelt(userId, bot)
    elif (itemId == '4'):
        return await FEUR()
    elif (itemId == '6'):
        return await ammo()

async def kickUser(userId, bot):
    member = findUser(bot, userId)
    await member.kick(reason="Connard")

def decrementeQuantity(userId, itemId):
    with open('data/inventory.json', 'r') as f:
        data = json.load(f)
        done = False

    for user in data:
        if user["userId"] == int (userId):
            for obj in user['objects']:
                if obj['obj'] == int (itemId):
                    if(obj['quantity'] == 1):
                        user['objects'].remove(obj)
                    else:
                        obj['quantity'] -= 1

                    done = True

    with open('data/inventory.json', 'w') as f:
        json.dump(data, f, indent=2)

    return done

async def throwRock(enemy, ctx):
    if(random.randint(0, 1) == 0):
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

        await deleteLastMessage(enemy, ctx)
    return {'embed': embed}

async def explosiveBelt(userId, bot):
    users = findUsers(bot)

    user1 = random.randint(0, len(users))
    user2 = random.randint(0, len(users))

    while (users[user1].id == users[user2].id
           or users[user1].id == int(userId)
           or users[user2].id == int(userId)
           or users[user1].id == 370295007057281024
           or users[user2].id == 370295007057281024
           or users[user1].id == 1303622459160924211
           or users[user2].id == 1303622459160924211

    ):
        user2 = random.randint(0, len(users))
        user1 = random.randint(0, len(users))

    await kickUser(users[user2].id, bot)
    await kickUser(users[user2].id, bot)
    await kickUser(int(userId), bot)


    embed = discord.Embed(
        title='EXPLOSION',
        description=f"<@{userId}> s'est suicidé. Et a emmené 2 connards : <@{users[user1].id}> et <@{users[user2].id}>",
        color=0xFF0000,
    )

    return {"embed": embed}

async def FEUR():
    embed = discord.Embed(
        title='QUOI ?',
        description=f"FEUR FEUR FEUR",
        color=0xFF0000,
    )

    return {'embed': embed}

async def ammo():
    embed = discord.Embed(
        title="Bien joué ! ",
        description=f"Tu as lancé la balle, mais t'as oublie de la mettre dans un glock...",
        color=0xFF0000,
    )

    return {'embed': embed}


async def deleteLastMessage(enemy, ctx):
    async for message in ctx.channel.history(limit=100):
        print(message)
        if message.author.id == int(enemy):
            await message.delete()
            return

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