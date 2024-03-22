# -*- coding: utf-8 -*-


import discord
from discord.ext import commands


class DiscordTools:
    
    @staticmethod
    def convert2files(paths: list[str]) -> list[discord.File]:
        return [discord.File(path) for path in paths]
    
    @staticmethod
    def get_role_choices(bot: commands.Bot):
        return [discord.app_commands.Choice(name=role.name, value=role.name) for guild in bot.guilds for role in guild.roles]