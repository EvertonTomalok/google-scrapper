# DEPRECATED

import asyncio
import json
from typing import Optional

import faust
import nest_asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

nest_asyncio.apply()

faust_app = faust.App(
    "google_executor",
    broker="localhost:9092",
    key_serializer="json",
    value_serializer="json",
)

store_topic = faust_app.topic("google_stores_to_crawl")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Store(BaseModel):
    ean: str
    name: str
    product_name: str
    product_price: float
    redirect_link: str
    system: Optional[str]


@app.get("/")
async def home():
    return "Google Store Service"


@app.get("/health")
async def health():
    return "Ok"


@app.post("/store/send", status_code=201)
async def store_send(store: Store):
    loop = asyncio.get_event_loop()
    r = loop.run_until_complete(await store_topic.send(value=store.json()))
    print(r)
    data = {
        "status": 201,
        "ok": True,
        "data": json.loads(store.json()),
    }
    return data
