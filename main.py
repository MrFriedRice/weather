from fastapi import FastAPI, Request

from fastapi.responses import HTMLResponse, JSONResponse

from fastapi.templating import Jinja2Templates

import csv

import aiohttp

import asyncio

app = FastAPI()

# 配置模板目录
templates = Jinja2Templates(directory='templates')

# 全局变量存储城市列表
cities = {}
def load_cities(file_path: str):
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cities[row["city"]] = {
                "latitude": float(row["latitude"]),
                "longitude": float(row["longitude"]),
            }
load_cities("europe.csv")

# 路由：返回 HTML 首页
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 路由：更新城市天气
@app.get("/update", response_class=JSONResponse)
async def update():
    return cities