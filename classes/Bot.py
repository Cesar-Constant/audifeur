import json
from abc import abstractmethod

import discord


class Bot:

    @staticmethod
    async def deleteLastMessage(ctx, enemy):
        async for message in ctx.channel.history(limit=100):
            if message.author.id == int(enemy):
                await message.delete()
                return

    @staticmethod
    def showItem(obj):
        embed = discord.Embed(
            title=obj['name'],
            description=obj['description'],
            color=0xFF0000,
        )

        file = discord.File(obj["url"], filename="image.png")
        embed.set_image(url="attachment://image.png")

        return {'embed': embed, 'file': file}

    @staticmethod
    def showError(title, message):
        embed = discord.Embed(
            title=title,
            description=message,
            color=0xFF0000,
        )

        file = discord.File('images/middleFinger.png', filename="image.png")
        embed.set_image(url="attachment://image.png")

        return {'embed': embed, 'file': file}

    @staticmethod
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

        if len(objects) == 0:
            embed.add_field(name='Rien', value="Y'a rien dans tes poches connard !", inline=False)

        else:
            with open('data/objects.json', 'r') as f:
                data = json.load(f)
                for o in objects:
                    for obj in data:
                        if (obj['id'] == o["obj"]):
                            title = f"[{obj['id']}] {obj['name']} X {o['quantity']}"
                            embed.add_field(name=title, value=obj['description'], inline=False)
        return embed