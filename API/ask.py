# -*- coding: utf-8 -*-


import g4f

from Types.response import MessageResponse
from Types.ask_models import AskModels


class Ask:
    
    @staticmethod
    async def get_answer(prompt: str, model: AskModels=AskModels.gpt_4) -> MessageResponse:
        try:
            answer = await g4f.ChatCompletion.create_async(
                model=model,
                messages=[{"role": "user", "content": f"{prompt}"}],
            )

            return MessageResponse(status=200, prompt=prompt, message=answer)
        except Exception as e:
            return MessageResponse(status=400, prompt=prompt, message="Возникла неизвестная ошибка при генерации ответа")