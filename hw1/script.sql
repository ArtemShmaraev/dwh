SELECT
    a.airport_code,
    COALESCE(flight_data.departure_flights_num, 0) AS departure_flights_num,
    COALESCE(flight_data.departure_psngr_num, 0) AS departure_psngr_num,
    COALESCE(flight_data.arrival_flights_num, 0) AS arrival_flights_num,
    COALESCE(flight_data.arrival_psngr_num, 0) AS arrival_psngr_num
FROM
    travel.airports a
        LEFT JOIN (
        SELECT
            f.departure_airport AS airport_code,
            COUNT(DISTINCT CASE WHEN f.departure_airport IS NOT NULL THEN f.flight_id END) AS departure_flights_num,
            COUNT(CASE WHEN f.departure_airport IS NOT NULL THEN tf.ticket_no END) AS departure_psngr_num,
            COUNT(DISTINCT CASE WHEN f.arrival_airport IS NOT NULL THEN f.flight_id END) AS arrival_flights_num,
            COUNT(CASE WHEN f.arrival_airport IS NOT NULL THEN tf.ticket_no END) AS arrival_psngr_num
        FROM
            travel.flights f
                LEFT JOIN travel.ticket_flights tf ON f.flight_id = tf.flight_id
        GROUP BY f.departure_airport, f.arrival_airport
    ) AS flight_data ON a.airport_code = flight_data.airport_code
ORDER BY a.airport_code;
