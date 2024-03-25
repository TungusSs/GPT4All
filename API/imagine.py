# -*- coding: utf-8 -*-


import os
import shutil

import wget
import discord
from loguru import logger
from gradio_client import Client

from Types.imagine_models import ImagineModels
from Types.response import ImageResponse


logger.add("GPT4All.log", format="{time} {level} {message}")


class Imagine:
    
    @staticmethod
    async def sdxl(prompt: str) -> str:
        logger.info(f"Отправка запроса '{prompt}' модели 'SDXL' на генерацию изображения.")
        client = Client("ByteDance/SDXL-Lightning", verbose=False, download_files=False)
        result = client.predict(
        	prompt,
        	"8-Step",
        	api_name="/generate_image"
        )
        
        logger.info(f"Сгенерированное изображение по запросу '{prompt}' модели 'SDXL' успешно получено")
        
        return result["url"]
    
    
    @staticmethod
    async def sd_cascade(prompt: str) -> str:
        logger.info(f"Отправка запроса '{prompt}' модели 'SD Cascade' на генерацию изображения.")
        client = Client("multimodalart/stable-cascade", verbose=False, download_files=False)
        result = client.predict(
        		prompt,	# str  in 'Prompt' Textbox component
        		"None",	# str  in 'Negative prompt' Textbox component
        		0,	# float (numeric value between 0 and 2147483647) in 'Seed' Slider component
        		1024,	# float (numeric value between 1024 and 1536) in 'Width' Slider component
        		1024,	# float (numeric value between 1024 and 1536) in 'Height' Slider component
        		10,	# float (numeric value between 10 and 30) in 'Prior Inference Steps' Slider component
        		0,	# float (numeric value between 0 and 20) in 'Prior Guidance Scale' Slider component
        		4,	# float (numeric value between 4 and 12) in 'Decoder Inference Steps' Slider component
        		0,	# float (numeric value between 0 and 0) in 'Decoder Guidance Scale' Slider component
        		1,	# float (numeric value between 1 and 2) in 'Number of Images' Slider component
        		api_name="/run"
        )
        
        logger.info(f"Сгенерированное изображение по запросу '{prompt}' модели 'SD Cascade' успешно получено")
        
        return result["url"]

    
    @staticmethod
    async def get_image(prompt: str, user_id: int, model: ImagineModels=ImagineModels.sdxl) -> ImageResponse:
        try:
            result = await Imagine.__func[model](prompt)
            logger.info(f"Загрузка сгенерированного изображения по запросу '{prompt}' модели '{model}'")
            
            wget.download(result, out=f"./cache/{user_id}/1.png", bar=None)
            logger.info(f"Изображение сгенерировано по запросу '{prompt}' модели '{model}' и загружено в папку для пользователя с ID '{user_id}'")
                
            return ImageResponse(
                status=200,
                message="Изображение сгенерировано.",
                prompt=prompt,
                file=f"./cache/{user_id}/1.png"
            )
        except Exception as e:
            logger.error(f"При получении изображения по запросу '{prompt}' модели '{model}' произошла ошибка: {e}")
            return ImageResponse(status=400, message=e, prompt=prompt, file=[])
    
    
    __func = {"sdxl": sdxl, "sd_cascade": sd_cascade}
