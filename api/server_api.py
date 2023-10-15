import math
import os
import random
import sqlite3
from io import BytesIO

import qrcode
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

lat_r = 0.00785
lon_r = 0.00525

app = FastAPI()
origins = ["*"]

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


def get_connection():
    return sqlite3.connect('data.db')


@app.post("/get_atm_location")
async def process_data(data: RequestData):
    index = 1
    res = await get_atm_locations(data.latitude, data.longitude, index)
    while len(res) < 1:
        if index > 100:
            return []
        
        index += 1
        res = await get_atm_locations(data.latitude, data.longitude, index)
    
    return res


async def get_atm_locations(latitude, longitude, index: int):
    lat_dt = lat_r * index
    lon_dt = lon_r * index
    
    connection = get_connection()
    cursor = connection.cursor()
    query = """SELECT * FROM `atm_data` WHERE latitude BETWEEN ? AND ? AND longitude BETWEEN ? AND ?;"""
    output_obj = cursor.execute(query, (latitude - lat_dt, latitude + lat_dt, longitude - lon_dt, longitude + lon_dt))
    rows = []
    
    for row in cursor.fetchall():
        rows.append({output_obj.description[i][0]: row[i] for i in range(len(row))})
    
    cursor.close()
    connection.close()
    
    return rows


@app.post("/get_office_location")
async def process_data(data: RequestData):
    index = 1
    points_nearby = await get_office_locations(data.latitude, data.longitude, index)
    while len(points_nearby) < 1:
        if index > 100:
            return []
        
        index += 1
        points_nearby = await get_office_locations(data.latitude, data.longitude, index)
    
    for point in points_nearby:
        point['loadingQueue'] = {}
        
        k, o = random.randint(5, 15), random.randint(0, 50)
        cel = (o // k)
        ost = 0 if o % k == 0 else 1
        
        if k * 1.5 >= o:
            st = "green"
        elif k * 2.5 >= o:
            st = "yellow"
        elif k * 3.5 >= o:
            st = "orange"
        else:
            st = "red"
        point['loadingQueue'] = [(cel + ost) * 10, st]
    
    return points_nearby


async def get_office_locations(latitude, longitude, index: int):
    lat_dt = lat_r * index
    lon_dt = lon_r * index
    
    connection = get_connection()
    cursor = connection.cursor()
    query = """SELECT * FROM `office_data` WHERE latitude BETWEEN ? AND ? AND longitude BETWEEN ? AND ?;"""
    output_obj = cursor.execute(query, (latitude - lat_dt, latitude + lat_dt, longitude - lon_dt, longitude + lon_dt))
    rows = []
    
    for row in cursor.fetchall():
        rows.append({output_obj.description[i][0]: row[i] for i in range(len(row))})
    
    cursor.close()
    connection.close()
    
    return rows


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
    
    return FileResponse(file_path, media_type="image/png",
                        headers={"Content-Disposition": f'attachment; filename="{q_code_name}"'})


class RequestDataTime(BaseModel):
    lat_p: float
    lon_p: float
    lat_vtb: float
    lon_vtb: float
    type_of_movement: int  # 0 пешком,  1 авто


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
    
    uvicorn.run(app, host="https://0.0.0.0", port=8000)
