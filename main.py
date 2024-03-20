# -*- coding: utf-8 -*-


import discord
from discord.ext import commands
from discord import Intents, app_commands
from decouple import config

from Utils.api import API


intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user.name} был подключён к Discord!")
    
    try:
        synced = await bot.tree.sync()
        print(f"Синхронизировано {len(synced)} команд.")
    except Exception as e:
        print(f"Возникла ошибка: {e}")

    await bot.wait_until_ready()


@bot.tree.command(name="gpt", description="Сгенерировать ответ на запрос.")
@app_commands.describe(prompt="Ваш запрос")
async def gpt(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer(ephemeral=True, thinking=True)
    
    response = await API.get_answer(prompt)
    
    await interaction.followup.send(f"*Ответ:*\n{response}")


# TODO: Реализовать генерацию изображений (пока не реализована)
@bot.tree.command(name="imagine", description="Сгенерировать изображение.")
@app_commands.describe(prompt="Ваш запрос")
async def imagine(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer(ephemeral=True, thinking=True)
    await interaction.followup.send(f"*⚠️ Эта команда временно не работает ⚠️*")


bot.run(config("DISCORD_TOKEN"))
