import random

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from config import bankomats, offices
import math

app = FastAPI()
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get_atm")
async def process_data():

    return bankomats[:10]


class RequestData(BaseModel):
    latitude: float
    longitude: float
@app.post("/get_atm_location")
async def process_data(data: RequestData):
    latitude_people = data.latitude
    longitude_people = data.longitude

    points_nearby = []
    len_points_nearby = []
    for bankomat in bankomats:
        ans = haversine(latitude_people, longitude_people, bankomat['latitude'], bankomat['longitude'])
        if ans < 15.0:
            bankomat['lenth'] = ans
            if len(points_nearby) == 5:
                max_value = max(len_points_nearby)
                index = len_points_nearby.index(max_value)

                len_points_nearby[index] = ans
                points_nearby[index] = bankomat
            else:
                points_nearby.append(bankomat)
                len_points_nearby.append(ans)

    return points_nearby

@app.post("/get_office_location")
async def process_data(data: RequestData):
    latitude_people = data.latitude
    longitude_people = data.longitude

    points_nearby = []
    len_points_nearby = []

    for office in offices:
        ans = haversine(latitude_people, longitude_people, office['latitude'], office['longitude'])
        if ans < 15.0:
            office['lenth'] = ans
            if len(points_nearby) == 5:
                max_value = max(len_points_nearby)
                index = len_points_nearby.index(max_value)

                len_points_nearby[index] = ans
                points_nearby[index] = office
            else:
                points_nearby.append(office)
                len_points_nearby.append(ans)

    for point in points_nearby:
        if 'loadingQueue' not in point:
            point['loadingQueue'] = {}

        for el in ['credit', 'card', 'mortgage', 'payments']:
            k, o = random.randint(5, 15), random.randint(0, 50)
            cel = (o // k)
            ost = 0 if o%k == 0 else 1

            if k * 1.5 >= o:
                st = "green"
            elif k * 2.5 >= o:
                st = "yellow"
            elif k * 3.5 >= o:
                st = "orange"
            else:
                st = "red"
            point['loadingQueue'][el] = [(cel+ost)*10, st]

    return points_nearby
    #loadingQueue credit card mortgage payments
def haversine(lat_p, lon_p, lat_vtb, lon_vtb):
    # Радиус Земли в километрах
    R = 6371.0

    # Переводим градусы в радианы
    lat1 = math.radians(lat_p)
    lon1 = math.radians(lon_p)
    lat2 = math.radians(lat_vtb)
    lon2 = math.radians(lon_vtb)

    # Разница в широте и долготе
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Вычисляем расстояние с использованием формулы Гаверсинуса
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance
if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="192.168.1.4", port=8000)
