# -*- coding: utf-8 -*-


from dataclasses import dataclass


@dataclass
class BaseResponse:
    status: int
    message: str
    prompt: str

@dataclass
class ImageResponse(BaseResponse):
    prompt: str
    file: str
    
@dataclass
class MessageResponse(BaseResponse):
    pass