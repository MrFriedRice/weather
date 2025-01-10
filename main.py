from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import aiohttp
import asyncio
import csv

app = FastAPI()

# 配置模板目录
templates = Jinja2Templates(directory="templates")

# 全局变量存储城市列表
cities = {}

# 加载城市列表
def load_cities(file_path: str):
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cities[row["city"]] = {
                "latitude": float(row["latitude"]),
                "longitude": float(row["longitude"]),
            }

load_cities("europe.csv")

# 获取单个城市天气数据
async def fetch_city_weather(city_name: str):
    city = cities[city_name]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={city['latitude']}&longitude={city['longitude']}&current_weather=true"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return {"name": city_name, "temp": data["current_weather"]["temperature"]}

# 路由：返回 HTML 首页
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 路由：更新城市天气
@app.get("/update", response_class=JSONResponse)
async def update_weather():
    tasks = [fetch_city_weather(city) for city in cities]
    results = await asyncio.gather(*tasks)
    return results