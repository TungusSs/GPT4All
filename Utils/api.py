# -*- coding: utf-8 -*-


import g4f


class API:

    models = g4f.models
    providers = g4f.Provider

    @staticmethod
    async def get_answer(prompt: str, model=models.gpt_4_turbo, provider=None) -> str:
        if provider:
            response = await g4f.ChatCompletion.create_async(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                provider=provider,
            )
        else:
            response = await g4f.ChatCompletion.create_async(
                model=model,
                messages=[{"role": "user", "content": prompt}],
            )

        return response