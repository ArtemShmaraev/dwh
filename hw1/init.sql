CREATE SCHEMA IF NOT EXISTS travel;

CREATE TABLE IF NOT EXISTS travel.bookings
(
    book_ref     CHAR(6) PRIMARY KEY,
    book_date    TIMESTAMPTZ    NOT NULL,
    total_amount NUMERIC(10, 2) NOT NULL
    );

CREATE TABLE IF NOT EXISTS travel.airports
(
    airport_code    CHAR(6) PRIMARY KEY,
    airport_name    TEXT             NOT NULL,
    city            TEXT             NOT NULL,
    coordinates_lon DOUBLE PRECISION NOT NULL,
    coordinates_lat DOUBLE PRECISION NOT NULL,
    timezone        TEXT             NOT NULL
    );

CREATE TABLE IF NOT EXISTS travel.aircrafts
(
    aircraft_code CHAR(6) PRIMARY KEY,
    model         JSONB   NOT NULL,
    range         INTEGER NOT NULL
    );

CREATE TABLE IF NOT EXISTS travel.tickets
(
    ticket_no      CHAR(13) PRIMARY KEY,
    book_ref       CHAR(6) REFERENCES travel.bookings (book_ref),
    passenger_id   VARCHAR(20) NOT NULL,
    passenger_name TEXT        NOT NULL,
    contact_data   JSONB
    );

CREATE TABLE IF NOT EXISTS travel.flights
(
    flight_id           SERIAL PRIMARY KEY,
    flight_no           CHAR(6)     NOT NULL,
    scheduled_departure TIMESTAMPTZ NOT NULL,
    scheduled_arrival   TIMESTAMPTZ NOT NULL,
    departure_airport   CHAR(6) REFERENCES travel.airports (airport_code),
    arrival_airport     CHAR(6) REFERENCES travel.airports (airport_code),
    status              VARCHAR(20),
    aircraft_code       CHAR(6) REFERENCES travel.aircrafts (aircraft_code),
    actual_departure    TIMESTAMPTZ,
    actual_arrival      TIMESTAMPTZ
    );

CREATE TABLE IF NOT EXISTS travel.ticket_flights
(
    ticket_no       CHAR(13) REFERENCES travel.tickets (ticket_no),
    flight_id       INTEGER REFERENCES travel.flights (flight_id),
    fare_conditions NUMERIC(10, 2)    NOT NULL,
    amount          NUMERIC(10, 2) NOT NULL,
    PRIMARY KEY (flight_id, ticket_no)
    );

CREATE TABLE IF NOT EXISTS travel.seats
(
    aircraft_code   CHAR(6) REFERENCES travel.aircrafts (aircraft_code),
    seat_no         VARCHAR(4)  NOT NULL,
    fare_conditions VARCHAR(10) NOT NULL,
    PRIMARY KEY (aircraft_code, seat_no)
    );

CREATE TABLE IF NOT EXISTS travel.boarding_passes
(
    ticket_no   CHAR(13) REFERENCES travel.tickets (ticket_no),
    flight_id   INTEGER REFERENCES travel.flights (flight_id),
    boarding_no INTEGER    NOT NULL,
    seat_no     VARCHAR(3) NOT NULL,
    PRIMARY KEY (flight_id, ticket_no)
    );
