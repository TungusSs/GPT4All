# -*- coding: utf-8 -*-


import os

import g4f
from discord.ext import commands
from discord import Intents

intents = Intents.default()
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user.name} был подключён к Discord!")


# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.errors.CheckFailure):
#         await ctx.send("При отправке команды вы не указали запрос.")


@bot.command(name="gpt")
async def gpt(ctx, *, args):
    if args:
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": args}],
            provider=g4f.Provider.Bing,
        )

        await ctx.send(f"{response}")
        # await ctx.send(f"Привет. Ты использовал команду `/gpt`. Так же ты мне написал текст: `{args}`")


# TODO: Реализовать генерацию изображений (пока не реализована).
@bot.command(name="imagine")
async def imagine(ctx, *, args):
    if args:
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": args}],
            provider=g4f.Provider.Bing,
        )

        await ctx.send(f"{response}")
        # await ctx.send(f"Привет. Ты использовал команду `/imagine`. Так же ты мне написал текст: `{args}`")


bot.run(os.getenv("DISCORD_TOKEN"))
