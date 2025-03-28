from fastapi import APIRouter, UploadFile, File, Form, Request, Response
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
import asyncio

import app.internal.ml.model as llm

from pydantic import BaseModel
from dotenv import load_dotenv
from dataclasses import dataclass

import os
import io
import json
import time

router = APIRouter(
    prefix="/api/v1"
)


@dataclass
class Generate(BaseModel):
    query: str



promt = """Сделай только примеры без комментариев в фомате и потом через раделитель <answer> решение:
1. \[\int x^2 \, dx = ?\]
2. d * e = ?
<answer>
1.\[\int x^2 \, dx = \frac{x^{3}}{3} + C\]
2. d * e = f
Тема на которую надо сделать примеры: """


@router.get("/generate")
async def generate(data: Generate):
    answer = llm.ollama(promt + data.query)
    return answer[answer.index("</think>")+8:]

