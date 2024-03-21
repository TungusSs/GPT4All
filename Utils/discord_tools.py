# -*- coding: utf-8 -*-


import discord


class DiscordTools:
    
    @staticmethod
    def convert2files(paths: list[str]) -> list[discord.File]:
        return [discord.File(path) for path in paths]