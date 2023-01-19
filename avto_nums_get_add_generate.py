import json
import psycopg2
from fastapi import FastAPI
import uvicorn
import re

app = FastAPI()


def get_connection():
    conn = psycopg2.connect(  # данные для подключения к базе данных
        host='localhost',
        user='postgres',
        password='123',
        database='Avto_nums',
    )
    conn.autocommit = True  # метод для внесения изменений в БД
    return conn


@app.get('/PLATE/GENERATE')   # (Генерация государственных номеров автомобилей)
def generate_avto_nums(token=None, amount: int | None = None):     # Bearer-токен авторизации, amount – количество государственных номеров автомобилей в ответе
    if token == None:
        return {'Токен не указан'}
    else:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""SELECT count(*) FROM avto_nums_data;""")
                amount = cursor.fetchall()[0][0]
        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
        finally:
            if connection:
                connection.close()

        return amount

@app.get('/PLATE/GET')  # (Получение государственных номеров автомобилей)
def get_avto_nums(id, token=None):  # token – Bearer-токен авторизации, id – идентификатор записи о государственном номере авто
    if token == None:
        return {'Токен не указан'}
    else:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT * FROM avto_nums_data
                WHERE id={id};""")
                response = cursor.fetchall()
        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
        finally:
            if connection:
                connection.close()

        return json.dumps(response)

@app.post('/PLATE/ADD')   # (Добавление государственных номеров автомобилей в базу данных)
def add_avto_nums_BD(token = None, plate: str = None):   # token – Bearer-токен авторизации, plate – государственный номер
    if token == None or plate == None:
        return {'token или plate не указан'}
    else:   # проверка на корректность номера
        if re.search(r'[^а-яА-Я0-9]', plate) == None and plate[0].isalpha() == True and plate[1:4].isdigit() == True and plate[4:6].isalpha() == True and plate[6:].isdigit() == True:   # проверка на корректность номера
            connection = get_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute(f"""INSERT INTO avto_nums_data(plate)
                    VALUES('{plate}');""")
            except Exception as _ex:
                print("[INFO] Error while working with PostgreSQL", _ex)
            finally:
                if connection:
                    connection.close()
                    return {f'Госномер {plate} добавлен в базу данных'}

        else:
            return {'Тип номера не соответствует стандарту'}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)