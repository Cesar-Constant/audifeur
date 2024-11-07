import discord
from discord.ext import commands
from classes.objects.Mutition import Munition
from classes.objects.Feur import Feur
from classes.objects.Caillou import Caillou
from classes.Bot import Bot
from classes.User import User

from func import ravus


intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.command(name='loot', description='Fouille les poubelles comme un clochard pour essayer de te sortir de ta vie de merde. Enculé !')
async def lootCommand(ctx):
    l = User.loot(ctx.author.id)
    await ctx.reply(embed=l['embed'], file=l['file'])

@bot.command(name='generate')
async def generateInventoryCommand(ctx):
    await User.generateInventory(bot)

@bot.command(name='inventory')
async def showInventoryCommand(ctx):
    await ctx.reply(embed=Bot.showInventory(ctx.author.id))

@bot.command(name='use')
async def useItemCommand(ctx):
    l = await User.useItem(ctx, bot)
    await ctx.reply(embed=l['embed'])


@bot.command(name='ravus')
async def useRavus(ctx):
    try:
        await ctx.reply(embed={ravus(ctx, bot)['embed']})
    except Exception as e:
        # If an error occurs, send an error message to the user
        await ctx.reply(f"Une erreur s'est produite : {e}")

@bot.command(name='lapidation')
async def useLapidation(ctx):
    try :
        enemy = ctx.message.content.split()[-1]
        ctx.message.content = "/use 3 "+ enemy
        for i in range(5):
            useItemCommand(ctx)

    except Exception as e:

        await ctx.reply(f"T'as pas assez de caillasses connard : {e}")



bot.run(TOKEN)