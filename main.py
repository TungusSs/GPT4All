# -*- coding: utf-8 -*-


import os

import discord
from discord.ext import commands
from discord import Intents, app_commands
from decouple import config

from Utils.api import API
from Utils.discord_tools import DiscordTools


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


@bot.tree.command(name="ask", description="Сгенерировать ответ на запрос.")
@app_commands.describe(prompt="Ваш запрос")
async def ask(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer(ephemeral=True, thinking=True)
    
    response = await API.get_answer(prompt)
    
    if response.status != 200:
        await interaction.followup.send(f"**Ваш запрос:** *{prompt}*\n**Результат**:*⚠️ {response.message} ⚠️*")
    else:
        await interaction.followup.send(f"**Ответ:**\n{response.message}")


@bot.tree.command(name="imagine", description="Сгенерировать изображения.")
@app_commands.describe(prompt="Ваш запрос")
async def imagine(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer(ephemeral=True, thinking=True)
    
    response = await API.get_image(prompt, interaction.user.id)
    
    if response.status != 200:
        await interaction.followup.send(f"**Ваш запрос:** *{prompt}*\n**Результат**:*⚠️ {response.message} ⚠️*")
    else:      
        files = DiscordTools.convert2files(response.files)
          
        await interaction.followup.send(f"**Ваш запрос:** *{prompt}*\n**Изображения:**", files=files)
        
        for image in response.files:
            os.remove(image)


@bot.tree.command(name="whois", description="Получить список пользователей с определённой ролью.")
@app_commands.describe(role_id="ID роли")
async def whois(interaction: discord.Interaction, role_id: str):
    await interaction.response.defer(ephemeral=True, thinking=True)

    # Проверяем, существует ли роль с таким ID
    role = discord.utils.get(interaction.guild.roles, id=int(role_id))
    if role is None:
        await interaction.followup.send("Роль не найдена.", ephemeral=True)
        return

    # Получаем список пользователей с этой ролью
    members_with_role = [member for member in interaction.guild.members if role in member.roles]

    # Формируем список в виде строки
    member_list = "\n".join([member.mention for member in members_with_role])

    # Отправляем список пользователю
    if member_list:
        await interaction.followup.send(f"Пользователи с ролью {role.name}:\n{member_list}", ephemeral=True)
    else:
        await interaction.followup.send(f"Нет пользователей с ролью {role.name}.", ephemeral=True)


bot.run(config("DISCORD_TOKEN"))
