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
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

current_guild = 1219544962949972051


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


async def roles_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    return DiscordTools.get_role_choices(bot)


@bot.tree.command(name="whois", description="Получить список пользователей с определённой ролью.")
@app_commands.describe(role_name="Название роли")
@app_commands.autocomplete(role_name=roles_autocomplete)
async def whois(interaction: discord.Interaction, role_name: str):
    await interaction.response.defer(ephemeral=True, thinking=True)
    
    try:
        current_role_id = [role.id for role in interaction.guild.roles if role.name == role_name][0]
    except IndexError:
        await interaction.followup.send(f"**В текущем канале нет ролей.**", ephemeral=True)
        return
    
    members_with_role = [member.mention for member in interaction.guild.members if member.get_role(current_role_id)]
    
    if not members_with_role:
        await interaction.followup.send(f"**Пользователи с ролью {role_name} не найдены.**", ephemeral=True)
        return
    
    await interaction.followup.send(f"**Все пользователи с ролью `{role_name}`:**\n{', '.join(members_with_role)}", ephemeral=True)


bot.run(config("DISCORD_TOKEN"))
