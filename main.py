# -*- coding: utf-8 -*-


import os
import asyncio

import discord
from loguru import logger
from decouple import config
from discord.ext import commands
from discord import Intents, app_commands

from API.ask import Ask
from API.imagine import Imagine


logger.add("GPT4All.log", format="{time} {level} {message}")

intents = Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)
tasks_queue = asyncio.Queue()

current_guild = 1219544962949972051


@bot.event
async def on_ready():
    logger.info(f"Бот {bot.user.name} был подключён к Discord!")
    
    bot.loop.create_task(process_tasks())
    
    try:
        synced = await bot.tree.sync()
        logger.info(f"Было синхронизировано {len(synced)} команд(ы)")
        
        if not os.path.exists("./cache/"):
            os.mkdir("./cache/")
            logger.info("Папка ./cache/ успешно создана")
    except Exception as e:
        logger.error(f"При выполнении синхронизации произошла ошибка: {e}")

    await bot.wait_until_ready()


@bot.tree.command(name="ask", description="Сгенерировать ответ на запрос.")
@app_commands.describe(prompt="Ваш запрос")
async def ask(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer(ephemeral=True, thinking=True)
    
    logger.info(f"Была получена команда /{interaction.command.name} от пользователя '{interaction.user.name}'")
    
    task = asyncio.create_task(Ask.get_answer(prompt))
    await tasks_queue.put(task)
    
    await task
    
    if task.result().status != 200:
        logger.error(f"При генерации ответа пользователю '{interaction.user.name}' произошла ошибка: {task.result().message}")
        await interaction.followup.send(f"**Ваш запрос:** *{prompt}*\n**Результат**:*⚠️ {task.result().message} ⚠️*")
    else:
        logger.info(f"Генерация ответа пользователю '{interaction.user.name}' прошла успешно")
        await interaction.followup.send(f"**Ваш запрос:** *{prompt}*\n**Ответ:**\n{task.result().message}")


@bot.tree.command(name="imagine", description="Сгенерировать изображение.")
@app_commands.describe(prompt="Ваш запрос")
async def imagine(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer(ephemeral=True, thinking=True)
    
    logger.info(f"Была получена команда /{interaction.command.name} от пользователя '{interaction.user.name}'")
    
    task = asyncio.create_task(Imagine.get_image(prompt, interaction.user.id))
    await tasks_queue.put(task)
    
    await task
    
    if task.result().status != 200:
        logger.error(f"При генерации изображения пользователю '{interaction.user.name}' произошла ошибка: {task.result().message}")
        await interaction.followup.send(f"**Ваш запрос:** *{prompt}*\n**Результат**:*⚠️ {task.result().message} ⚠️*")
    else:         
        logger.info(f"Генерация изображения пользователю '{interaction.user.name}' прошла успешно")
        await interaction.followup.send(f"**Ваш запрос:** *{prompt}*\n**Изображение:**", file=discord.File(task.result().file))

        os.remove(task.result().file)
        logger.info(f"Файл {task.result().file} был удален")


async def roles_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    return [app_commands.Choice(name=role.name, value=role.name) for guild in bot.guilds for role in guild.roles]


@bot.tree.command(name="whois", description="Получить список пользователей с определённой ролью.")
@app_commands.describe(role_name="Название роли")
@app_commands.autocomplete(role_name=roles_autocomplete)
async def whois(interaction: discord.Interaction, role_name: str):
    await interaction.response.defer(ephemeral=True, thinking=True)
    
    logger.info(f"Была получена команда /{interaction.command.name} от пользователя '{interaction.user.name}'")
    
    try:
        current_role_id = [role.id for role in interaction.guild.roles if role.name == role_name][0]
    except IndexError:
        await interaction.followup.send(f"**В текущем канале нет ролей.**", ephemeral=True)
        return
    
    members_with_role = [member.mention for member in interaction.guild.members if member.get_role(current_role_id)]
    
    if not members_with_role:
        await interaction.followup.send(f"**Пользователи с ролью {role_name} не найдены.**", ephemeral=True)
        return
    
    logger.info(f"Пользователь '{interaction.user.name}' успешно получил список ролей по названию '{role_name}'")
    
    await interaction.followup.send(f"**Все пользователи с ролью `{role_name}`:**\n{', '.join(members_with_role)}", ephemeral=True)


@bot.tree.command(name="help", description="Информация по командам бота")
async def help(interaction: discord.Interaction):
    logger.info(f"Была получена команда /{interaction.command.name} от пользователя '{interaction.user.name}'")
    
    embed = discord.Embed(
        title="Общая информация о боте",
        description="Здесь вы можете найти информацию о командах",
        color=0x6698a9
    )

    embed.add_field(
        name="/ask",
        value="Сгенерировать ответ на запрос.\nИспользуйте: `/ask Ваш запрос`",
        inline=False
    )
    embed.add_field(
        name="/imagine",
        value="Сгенерировать изображение по запросу.\nИспользуйте: `/imagine Ваш запрос`",
        inline=False
    )

    embed.add_field(
        name="/whois",
        value="Отобразить всех пользователей с определенной ролью.\nИспользуйте: `/whois Название роли`",
        inline=False
    )

    embed.add_field(
        name="Разработчики",
        value="Информация о разработчиках и ссылки на их социальные сети",
        inline=False
    )
    embed.add_field(
        name="Tungus",
        value="[Telegram](https://t.me/ArnoVictorDorianne)\n[GitHub](https://github.com/TungusSs)\n[LinkedIn](https://www.linkedin.com/in/nikitakuznetsovv/)",
        inline=True
    )
    embed.add_field(
        name="Oustery",
        value="[Telegram](https://t.me/Oustery)\n[GitHub](https://github.com/oustery)",
        inline=True
    )

    embed.add_field(
        name="GitHub проекта",
        value="[GitHub](https://github.com/TungusSs/GPT4All)",
        inline=False
    )

    embed.set_thumbnail(url="https://cdn.discordapp.com/app-icons/1219539189310427136/333f190e10a39605f26552afe8a18322.png?size=256&quot")

    embed.set_footer(text="Бот разработан с ❤️ командой разработчиков")
    
    logger.info(f"Пользователь '{interaction.user.name}' успешно получил вспомогательную информацию о боте")

    await interaction.response.send_message(embed=embed, ephemeral=True)


async def process_tasks():
    while True:
        task = await tasks_queue.get()
        try:
            await task
        except Exception as e:
            logger.error(f"Ошибка при попытке выполнить задачу: {e}")
        finally:
            tasks_queue.task_done()
            

bot.run(config("DISCORD_TOKEN"))
