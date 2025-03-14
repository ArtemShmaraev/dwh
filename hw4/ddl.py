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

# DDL-скрипт для создания таблиц
ddl_script = """
CREATE TABLE airports (
    airport_code CHAR(3) PRIMARY KEY,
    airport_name TEXT NOT NULL,
    city TEXT NOT NULL,
    coordinates_lon DOUBLE PRECISION,
    coordinates_lat DOUBLE PRECISION,
    timezone TEXT
);

CREATE TABLE bookings (
    book_ref CHAR(6) PRIMARY KEY,
    book_date TIMESTAMPTZ NOT NULL,
    total_amount NUMERIC(10,2) NOT NULL
);

CREATE TABLE tickets (
    ticket_no CHAR(13) PRIMARY KEY,
    book_ref CHAR(6) REFERENCES bookings(book_ref) ON DELETE CASCADE,
    passenger_id VARCHAR(20),
    passenger_name TEXT NOT NULL,
    contact_data JSONB
);

CREATE TABLE flights (
    flight_id SERIAL PRIMARY KEY,
    flight_no CHAR(6),
    scheduled_departure TIMESTAMPTZ NOT NULL,
    scheduled_arrival TIMESTAMPTZ NOT NULL,
    departure_airport CHAR(3) REFERENCES airports(airport_code),
    arrival_airport CHAR(3) REFERENCES airports(airport_code),
    status VARCHAR(20),
    aircraft_code CHAR(3),
    actual_departure TIMESTAMPTZ,
    actual_arrival TIMESTAMPTZ
);

CREATE TABLE ticket_flights (
    ticket_no CHAR(13) REFERENCES tickets(ticket_no) ON DELETE CASCADE,
    flight_id INTEGER REFERENCES flights(flight_id) ON DELETE CASCADE,
    fare_conditions VARCHAR(10),
    amount NUMERIC(10,2),
    PRIMARY KEY (flight_id, ticket_no)
);

CREATE TABLE boarding_passes (
    ticket_no CHAR(13) REFERENCES tickets(ticket_no) ON DELETE CASCADE,
    flight_id INTEGER REFERENCES flights(flight_id) ON DELETE CASCADE,
    boarding_no INTEGER,
    seat_no VARCHAR(4),
    PRIMARY KEY (flight_id, ticket_no)
);

CREATE TABLE aircrafts (
    aircraft_code CHAR(3) PRIMARY KEY,
    model JSONB,
    range INTEGER NOT NULL
);

CREATE TABLE seats (
    aircraft_code CHAR(3) REFERENCES aircrafts(aircraft_code) ON DELETE CASCADE,
    seat_no VARCHAR(4),
    fare_conditions VARCHAR(10),
    PRIMARY KEY (aircraft_code, seat_no)
);
"""

# Выполняем DDL-скрипт
cur.execute(ddl_script)

# Фиксируем изменения и закрываем соединение
conn.commit()
cur.close()
conn.close()

print("✅ Таблицы успешно созданы!")
