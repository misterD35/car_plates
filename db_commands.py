import psycopg2


connection, cursor = 0, 0
try:
    connection = psycopg2.connect(  # данные для подключения к базе данных
        host='localhost',
        user='postgres',
        password='123',
        database='Avto_nums',
    )


    # СОЗДАТЬ ТАБЛИЦУ
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE avto_nums_data(
                 id serial NOT NULL PRIMARY KEY,
                 plate varchar NOT NULL);""")
    connection.commit()
    print("[INFO] Table created successfully")

    # ВСТАВИТЬ ЗНАЧЕНИЯ
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO avto_nums_data(plate)
                    VALUES('Р345ШЛ234'),
                    ('В847УТ34'),
                    ('Р932УН197');""")
    connection.commit()
    print("[INFO] Table created successfully")

    # УДАЛЕНИЕ ТАБЛИЦЫ/СТРОКИ ПО УСЛОВИЮ ИЗ ТАБЛИЦЫ
    cursor = connection.cursor()
    cursor.execute("""DROP TABLE avto_nums_data;""")
    connection.commit()
    print("[INFO] String was deleted")



except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print("[INFO] PostgreSQL connection closed")