# k = 15
# o = 22
#
# cel = (o // k)
# ost = 0 if o%k == 0 else 1
#
# if k * 1.5 >= o:
#     st = "green"
# elif k * 2.5 >= o:
#     st = "yellow"
# elif k * 3.5 >= o:
#     st = "orange"
# else:
#     st = "red"
#
# print(st)
#
#
# print((cel+ost)*10)
import math


def haversine(lat1, lon1, lat2, lon2):
    # Радиус Земли в километрах
    R = 6371.0

    # Переводим градусы в радианы
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Разница в широте и долготе
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Вычисляем расстояние с использованием формулы Гаверсинуса
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance

# Пример использования 'latitude': 55.880677, 'longitude': 37.558643, 'latitude': 55.745726, 'longitude': 37.625702,
lat1 = 55.880677
lon1 = 37.558643
lat2 = 55.745726
lon2 = 37.625702

distance = haversine(lat1, lon1, lat2, lon2)
print(f"Расстояние между точками: {distance} км")