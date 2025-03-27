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
    model_type: str




@router.post("/generate")
async def generate(data: Generate):
    llm.ollama(data.query)

