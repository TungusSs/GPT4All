# -*- coding: utf-8 -*-


import os
import asyncio

import discord
from discord.ext import commands
from discord import Intents, app_commands
from decouple import config

from API.ask import Ask
from API.imagine import Imagine
from Utils.discord_tools import DiscordTools


intents = Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)
tasks_queue = asyncio.Queue()

current_guild = 1219544962949972051


@bot.event
async def on_ready():
    print(f"{bot.user.name} был подключён к Discord!")
    
    bot.loop.create_task(process_tasks())
    
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
    
    task = asyncio.create_task(Ask.get_answer(prompt))
    await tasks_queue.put(task)
    
    await task
    
    if task.result().status != 200:
        await interaction.followup.send(f"**Ваш запрос:** *{prompt}*\n**Результат**:*⚠️ {task.result().message} ⚠️*")
    else:
        await interaction.followup.send(f"**Ответ:**\n{task.result().message}")


@bot.tree.command(name="imagine", description="Сгенерировать изображение.")
@app_commands.describe(prompt="Ваш запрос")
async def imagine(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer(ephemeral=True, thinking=True)
    
    task = asyncio.create_task(Imagine.get_image(prompt, interaction.user.id))
    await tasks_queue.put(task)
    
    await task
    
    if task.result().status != 200:
        await interaction.followup.send(f"**Ваш запрос:** *{prompt}*\n**Результат**:*⚠️ {task.result().message} ⚠️*")
    else:         
        await interaction.followup.send(f"**Ваш запрос:** *{prompt}*\n**Изображение:**", file=discord.File(task.result().file))

        os.remove(task.result().file)


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


async def process_tasks():
    while True:
        task = await tasks_queue.get()
        try:
            await task
        except Exception as e:
            print(f"Ошибка при выполнении задачи: {e}")
        finally:
            tasks_queue.task_done()
            

bot.run(config("DISCORD_TOKEN"))
