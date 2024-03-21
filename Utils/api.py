# -*- coding: utf-8 -*-


import os

import g4f
import discord
from decouple import config
from EdgeGPT.ImageGen import ImageGenAsync

from Types.response import BaseResponse, ImageResponse, MessageResponse


class API:

    models = g4f.models
    providers = g4f.Provider

    @staticmethod
    async def get_answer(prompt: str, model=models.gpt_4_turbo, provider=None) -> MessageResponse:
        try:
            if provider:
                answer = await g4f.ChatCompletion.create_async(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    provider=provider,
                )
            else:
                answer = await g4f.ChatCompletion.create_async(
                    model=model,
                    messages=[{"role": "user", "content": f"{prompt}"}],
                )

            return MessageResponse(status=200, prompt=prompt, message=answer)
        except Exception as e:
            return MessageResponse(status=400, prompt=prompt, message="Возникла неизвестная ошибка при генерации ответа")

        
    
    @staticmethod
    async def get_image(prompt: str, user_id: int) -> ImageResponse:
        try:
            image_generator = ImageGenAsync(config("U_COOKIE"), False)
            
            images = await image_generator.get_images(prompt=prompt)
            await image_generator.save_images(images, download_count=2, output_dir=f"./cache/{user_id}/")
                
            return ImageResponse(
                status=200,
                message="Изображения сгенерированы.",
                prompt=prompt,
                files=[os.path.join(f"./cache/{user_id}/", image) for image in os.listdir(f"./cache/{user_id}/")]
            )
        except Exception as e:
            print(e)
            
            if "blocked" in e.args[0]:
                return ImageResponse(status=401, message="Запрос содержит запрещённые слова", prompt=prompt, files=[])
            else:
                return ImageResponse(status=400, message="Возникла неизвестная ошибка при генерации изображений", prompt=prompt, files=[])