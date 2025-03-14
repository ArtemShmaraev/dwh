import psycopg2

# Подключение к БД
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="mypassword",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Список таблиц для удаления данных
tables = [
    'boarding_passes',
    'ticket_flights',
    'seats',
    'aircrafts',
    'flights',
    'tickets',
    'bookings',
    'airports'
]

# Для каждой таблицы выполняем команду DELETE
for table in tables:
    cur.execute(f"DELETE FROM {table};")
    print(f"✅ Данные из таблицы {table} удалены!")

# Фиксируем изменения и закрываем соединение
conn.commit()
cur.close()
conn.close()

print("✅ Все данные успешно удалены из таблиц!")
