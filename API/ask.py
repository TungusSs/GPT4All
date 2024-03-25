# -*- coding: utf-8 -*-


import g4f

from loguru import logger

from Types.response import MessageResponse
from Types.ask_models import AskModels


logger.add("GPT4All.log", format="{time} {level} {message}")


class Ask:
    
    @staticmethod
    async def get_answer(prompt: str, model: AskModels=AskModels.gpt_4) -> MessageResponse:
        try:
            logger.info(f"Отправка запроса '{prompt}' модели '{model.name}' на генерацию ответа")
            
            answer = await g4f.ChatCompletion.create_async(
                model=model,
                messages=[{"role": "user", "content": f"{prompt}"}],
            )
            
            logger.info(f"Ответ на запрос '{prompt}' модели '{model.name}' на генерацию ответа успешно получен.")

            return MessageResponse(status=200, prompt=prompt, message=answer)
        except Exception as e:
            logger.error(f"При получении ответа по запросу '{prompt}' произошла ошибка: {e}")
            return MessageResponse(status=400, prompt=prompt, message=e)