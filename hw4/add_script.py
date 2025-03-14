import psycopg2
from faker import Faker
import random
import json
from datetime import datetime, timedelta

# Подключение к БД
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="mypassword",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

faker = Faker()
Faker.seed(42)
random.seed(42)

# Функция для генерации случайной даты за последние два месяца
def generate_random_date_within_last_two_months():
    today = datetime.today()
    two_months_ago = today - timedelta(days=60)  # 60 дней назад (приблизительно 2 месяца)
    return faker.date_between(start_date=two_months_ago, end_date=today)

# Генерация аэропортов (22 аэропорта)
airport_data = [
    ("JFK", "John F. Kennedy International Airport", "New York", -73.7781, 40.6413, "America/New_York"),
    ("LHR", "Heathrow Airport", "London", -0.4543, 51.4700, "Europe/London"),
    ("DXB", "Dubai International Airport", "Dubai", 55.3644, 25.276987, "Asia/Dubai"),
    ("LAX", "Los Angeles International Airport", "Los Angeles", -118.4085, 33.9416, "America/Los_Angeles"),
    ("ORD", "O'Hare International Airport", "Chicago", -87.9048, 41.9742, "America/Chicago"),
    ("HKG", "Hong Kong International Airport", "Hong Kong", 113.9185, 22.3080, "Asia/Hong_Kong"),
    ("SIN", "Singapore Changi Airport", "Singapore", 103.9940, 1.3644, "Asia/Singapore"),
    ("AMS", "Amsterdam Airport Schiphol", "Amsterdam", 4.7632, 52.3105, "Europe/Amsterdam"),
    ("CDG", "Charles de Gaulle Airport", "Paris", 2.5522, 49.0097, "Europe/Paris"),
    ("FRA", "Frankfurt Airport", "Frankfurt", 8.5706, 50.0379, "Europe/Berlin"),
    ("SYD", "Sydney Kingsford Smith Airport", "Sydney", 151.1772, -33.8688, "Australia/Sydney"),
    ("ICN", "Incheon International Airport", "Seoul", 126.4501, 37.4602, "Asia/Seoul")
]
airport_codes = [airport[0] for airport in airport_data]
for airport in airport_data:
    cursor.execute(
        "INSERT INTO airports (airport_code, airport_name, city, coordinates_lon, coordinates_lat, timezone) VALUES (%s, %s, %s, %s, %s, %s)",
        (airport[0], airport[1], airport[2], airport[3], airport[4], airport[5])
    )

# Генерация самолетов (6 моделей)
aircraft_codes = [faker.unique.bothify(text="???").upper() for _ in range(6)]
for code in aircraft_codes:
    model = {"name": faker.company(), "type": random.choice(["Boeing", "Airbus", "Embraer"])}
    cursor.execute(
        "INSERT INTO aircrafts (aircraft_code, model, range) VALUES (%s, %s, %s)",
        (code, json.dumps(model), random.randint(500, 15000))
    )

# Генерация бронирований (700 бронирований)
book_refs = [faker.unique.bothify(text="######") for _ in range(700)]
for book_ref in book_refs:
    cursor.execute(
        "INSERT INTO bookings (book_ref, book_date, total_amount) VALUES (%s, %s, %s)",
        (book_ref, generate_random_date_within_last_two_months(), round(random.uniform(100, 2000), 2))
    )

# Генерация пассажиров (5000 пассажиров, у каждого может быть несколько билетов)
passengers = [faker.unique.uuid4()[:20] for _ in range(5000)]
ticket_nos = [faker.unique.bothify(text="?????????????")[:13] for _ in range(700)]  # 700 билетов
for ticket_no in ticket_nos:
    passenger_id = random.choice(passengers)
    cursor.execute(
        "INSERT INTO tickets (ticket_no, book_ref, passenger_id, passenger_name, contact_data) VALUES (%s, %s, %s, %s, %s)",
        (ticket_no, random.choice(book_refs), passenger_id, faker.name(), json.dumps({"email": faker.email()}))
    )

# Генерация рейсов (50 рейсов)
flight_ids = []
for _ in range(50):
    departure_airport, arrival_airport = random.sample(airport_codes, 2)
    scheduled_departure = generate_random_date_within_last_two_months()
    scheduled_arrival = scheduled_departure + timedelta(hours=random.randint(1, 10))
    cursor.execute(
        "INSERT INTO flights (flight_no, scheduled_departure, scheduled_arrival, departure_airport, arrival_airport, status, aircraft_code) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING flight_id",
        (
            faker.unique.bothify(text="??????").upper(),
            scheduled_departure,
            scheduled_arrival,
            departure_airport,
            arrival_airport,
            random.choice(["Scheduled", "Delayed", "Cancelled"]),
            random.choice(aircraft_codes)
        )
    )
    flight_ids.append(cursor.fetchone()[0])

# Генерация билетов для рейсов (каждый пассажир может участвовать в нескольких рейсах)
for ticket_no in ticket_nos:
    flights_for_ticket = random.randint(1, 3)  # 1-3 рейса на одного пассажира
    chosen_flights = set()  # Используем множество для уникальности рейсов
    for _ in range(flights_for_ticket):
        # Выбираем случайный рейс, пока не найдём уникальный
        flight_id = random.choice(flight_ids)
        while (ticket_no, flight_id) in chosen_flights:
            flight_id = random.choice(flight_ids)
        chosen_flights.add((ticket_no, flight_id))

        cursor.execute(
            "INSERT INTO ticket_flights (ticket_no, flight_id, fare_conditions, amount) VALUES (%s, %s, %s, %s)",
            (ticket_no, flight_id, random.choice(["Economy", "Business", "First"]), round(random.uniform(100, 5000), 2))
        )

# Генерация посадочных талонов (исключаем дублирование рейсов)
cursor.execute("SELECT ticket_no, flight_id FROM ticket_flights")
ticket_flight_map = cursor.fetchall()
for ticket_no, flight_id in ticket_flight_map:
    cursor.execute(
        "INSERT INTO boarding_passes (ticket_no, flight_id, boarding_no, seat_no) VALUES (%s, %s, %s, %s)",
        (ticket_no, flight_id, random.randint(1, 200), faker.bothify(text="##"))
    )

# Генерация мест в самолетах (по 30 мест в каждом самолете)
for code in aircraft_codes:
    for i in range(1, 31):
        cursor.execute(
            "INSERT INTO seats (aircraft_code, seat_no, fare_conditions) VALUES (%s, %s, %s)",
            (code, f"{i}{random.choice('ABCD')}", random.choice(["Economy", "Business", "First"]))
        )

# Коммит изменений и закрытие соединения
conn.commit()
cursor.close()
conn.close()

print("✅ База данных успешно заполнена фейковыми данными!")
