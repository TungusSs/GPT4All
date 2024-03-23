# -*- coding: utf-8 -*-


from dataclasses import dataclass


@dataclass
class ImagineModels:
    sdxl: str = "sdxl"
    playground: str = "playground"
    sd_cascade: str = "sd-cascade"