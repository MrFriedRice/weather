from fastapi import FastAPI, Request

from fastapi.responses import HTMLResponse, JSONResponse

from fastapi.templating import Jinja2Templates

import csv

import aiohttp

app = FastAPI()

templates = Jinja2Templates(directory='templates')

cities = []


def load_cities(file_path: str):
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cities.append({
                "city": row["city"],
                "latitude": row["latitude"],
                "longitude": row["longitude"]
            })


load_cities("europe.csv")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/getAll", response_class=JSONResponse)
async def update():
    latitude = ",".join([row["latitude"] for row in cities])
    longitude = ",".join([row["longitude"] for row in cities])
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            for index, row in enumerate(data):
                row['city'] = cities[index]['city']
            return data


@app.get("/getInfo", response_class=JSONResponse)
async def getInfo(request: Request):
    latitude = request.query_params.get("latitude")
    longitude = request.query_params.get("longitude")
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
