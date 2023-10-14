import os
import random

import qrcode
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse

from config import bankomats, offices
import math
from io import BytesIO


app = FastAPI()
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

        bankomat['lenth'] = ans
        if len(points_nearby) == 5:
            max_value = max(len_points_nearby)
            index = len_points_nearby.index(max_value)

            len_points_nearby[index] = ans
            points_nearby[index] = bankomat
        else:
            points_nearby.append(bankomat)
            len_points_nearby.append(ans)

        min_len = float('inf')
        max_len = 0
        for point in points_nearby:
            min_len = min(min_len, point['lenth'])
            max_len = max(max_len, point['lenth'])
        midele = int((min_len + max_len))//2

        ans = []
        for point in points_nearby:
            if midele > point['lenth']:
                ans.append(point)
    return ans


@app.post("/get_office_location")
async def process_data(data: RequestData):
    latitude_people = data.latitude
    longitude_people = data.longitude

    points_nearby = []
    len_points_nearby = []

    for office in offices:
        ans = haversine(latitude_people, longitude_people, office['latitude'], office['longitude'])

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

        point['loadingQueue'] = {}

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
        point['loadingQueue'] = [(cel+ost)*10, st]

        min_len = float('inf')
        max_len = 0

        for point in points_nearby:
            min_len = min(min_len, point['lenth'])
            max_len = max(max_len, point['lenth'])
        midele = int((min_len + max_len)) // 2

        ans = []
        for point in points_nearby:
            if midele > point['lenth']:
                ans.append(point)

    return ans


@app.get("/get_q_code")
async def process_data():
    data = "Информация о клиенте и о банке где взял талон"
    qr = qrcode.make(data)

    # Сохраняем QR-код в байты
    img_byte_array = BytesIO()
    qr.save(img_byte_array, format="PNG")
    img_byte_array.seek(0)

    # Удаляем файл (если он существует)
    file_path = "q-code/some_file.png"
    if os.path.exists(file_path):
        os.remove(file_path)

    # Генерируем имя файла (название QR-кода)
    q_code_name = f"O-{random.randint(0, 50)}.png"

    # Сохраняем изображение как файл
    with open(file_path, "wb") as file:
        file.write(img_byte_array.read())

    return FileResponse(file_path, media_type="image/png", headers={"Content-Disposition": f'attachment; filename="{q_code_name}"'})


class RequestDataTime(BaseModel):
    lat_p: float
    lon_p: float
    lat_vtb: float
    lon_vtb: float
    type_of_movement: int # 0 пешком,  1 авто

@app.post("/get_time")
async def process_data(data: RequestDataTime):
    lat_p = data.lat_p
    lon_p = data.lon_p
    lat_vtb = data.lat_vtb
    lon_vtb = data.lon_vtb
    type_of_movement = data.type_of_movement

    if type_of_movement:
        speed = 40
    else:
        speed = 6

    km_len = haversine(lat_p, lon_p, lat_vtb, lon_vtb)

    return calculate_travel_time(km_len, speed)


def calculate_travel_time(km_len, speed):
    hours = int(km_len / speed)
    minutes = int((km_len / speed - hours) * 60)
    return f"{hours} ч. {minutes:02d} мин."

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
