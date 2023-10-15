import math
import sqlite3

import config

sqlite_create = '''CREATE TABLE IF NOT EXISTS atm_data (id INTEGER PRIMARY KEY, address VARCHAR,
    latitude FLOAT, longitude FLOAT, all_day BIT);'''

sqlite_create0 = '''CREATE TABLE IF NOT EXISTS office_data (id INTEGER PRIMARY KEY, salePointName VARCHAR,
    address VARCHAR, latitude FLOAT, longitude FLOAT, distance INTEGER, x FLOAT, y FLOAT,
    rko VARCHAR, officeType VARCHAR, salePointFormat VARCHAR, suoAvailability BIT, hasRamp BIT,
    metroStation VARCHAR, kep VARCHAR);'''


def get_connection():
    return sqlite3.connect('data.db')


def close_connection(connection: sqlite3.Connection):
    if connection:
        connection.close()


def parse():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        for data in config.bankomats:
            query = """INSERT INTO `atm_data` (`address`, `latitude`, `longitude`, `all_day`) VALUES (?,?,?,?);"""
            cursor.execute(query, (data['address'], data['latitude'], data['longitude'], data['allDay']))
        connection.commit()
        cursor.close()
        connection.close()
    except (Exception, sqlite3.Error) as error:
        print("Error while getting data", error)


def parse0():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        for data in config.offices:
            query = """INSERT INTO `office_data` (`salePointName`, `address`, `latitude`,
            `longitude`, `distance`, `x`, `y`, `rko`, `officeType`, `salePointFormat`, `suoAvailability`,
            `hasRamp`, `metroStation`, `kep`) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);"""
            
            x, y = lon_lat_to_mercator(data['longitude'], data['latitude'])
            
            cursor.execute(query, (
                data['salePointName'], data['address'], data['latitude'], data['longitude'], data['distance'],
                x, y,
                'Неизвестно' if data['rko'] is None else data['rko'].capitalize(),
                data['officeType'].capitalize(), data['salePointFormat'],
                'Есть' if data['suoAvailability'] == 'Y' else (
                    'Нет' if data['suoAvailability'] == 'N' else 'Неизвестно'),
                'Есть' if data['hasRamp'] == 'Y' else ('Нет' if data['hasRamp'] == 'N' else 'Неизвестно'),
                'Нет' if data['metroStation'] is None else data['metroStation'],
                'Есть' if data['kep'] is True else ('Нет' if data['kep'] is False else 'Неизвестно')
            ))
        connection.commit()
        cursor.close()
        connection.close()
    except (Exception, sqlite3.Error) as error:
        print("Error while getting data", error)


def lon_lat_to_mercator(lon, lat):
    R = 6371000
    x = R * math.radians(lon)
    y = R * math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
    return x, y


con = get_connection()
cur = con.cursor()
con.execute(sqlite_create)
con.execute(sqlite_create0)
con.commit()
cur.close()

parse()
parse0()

con.commit()
cur.close()
con.close()
