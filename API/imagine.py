# -*- coding: utf-8 -*-


import os
import shutil

import discord
from gradio_client import Client

from Types.imagine_models import ImagineModels
from Types.response import ImageResponse


class Imagine:
    
    @staticmethod
    async def sdxl(prompt: str) -> str:
        client = Client("ByteDance/SDXL-Lightning")
        result = client.predict(
        	prompt,
        	"8-Step",
        	api_name="/generate_image"
        )
        
        return result


    @staticmethod
    async def playground(prompt: str) -> str:
        client = Client("https://playgroundai-playground-v2-5.hf.space/--replicas/amkzc/")
        result = client.predict(
        		prompt,	# str  in 'Prompt' Textbox component
        		"None",	# str  in 'Negative prompt' Textbox component
        		True,	# bool  in 'Use negative prompt' Checkbox component
        		0,	# float (numeric value between 0 and 2147483647) in 'Seed' Slider component
        		1024,	# float (numeric value between 256 and 1536) in 'Width' Slider component
        		1024,	# float (numeric value between 256 and 1536) in 'Height' Slider component
        		0.6,	# float (numeric value between 0.1 and 20) in 'Guidance Scale' Slider component
        		True,	# bool  in 'Randomize seed' Checkbox component
        		api_name="/run"
        )
        
        return result[0][0]["image"]
    
    
    @staticmethod
    async def sd_cascade(prompt: str) -> str:
        client = Client("multimodalart/stable-cascade")
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
        
        return result

    
    @staticmethod
    async def get_image(prompt: str, user_id: int, model: ImagineModels=ImagineModels.sdxl) -> ImageResponse:
        try:
            result = await Imagine.__func[model](prompt)
            
            os.mkdir(f"./cache/{user_id}")
            shutil.move(result, f"./cache/{user_id}/1.png")
                
            return ImageResponse(
                status=200,
                message="Изображения сгенерированы.",
                prompt=prompt,
                file=f"./cache/{user_id}/1.png"
            )
        except Exception as e:
            print(e)
        
            return ImageResponse(status=400, message="Возникла неизвестная ошибка при генерации изображений", prompt=prompt, file=[])
    
    
    __func = {"sdxl": sdxl, "playground": playground, "sd_cascade": sd_cascade}
