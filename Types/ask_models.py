# -*- coding: utf-8 -*-


import g4f
from dataclasses import dataclass


@dataclass
class AskModels:
    gpt_4: str = g4f.models.gpt_4
    gpt_4_turbo: str = g4f.models.gpt_4_turbo
    gemini_pro: str = g4f.models.gemini_pro