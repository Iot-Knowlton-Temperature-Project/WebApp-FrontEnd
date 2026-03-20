import mysql.connector


def query_sensor_statuses(timeout_seconds=120):
    statuses = {
        1: ("Unknown", "0", "0", "0"),
        2: ("Unknown", "0", "0", "0"),
        3: ("Unknown", "0", "0", "0"),
        4: ("Unknown", "0", "0", "0"),
        5: ("Unknown", "0", "0", "0"),
    }

    try:
        connection = mysql.connector.connect(
            host="PI-26-IOT", 
            user="user",
            password="changeme",
            database="esp"
        )

        if connection.is_connected():
            print("Successfully connected")
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT
                    sensor_id,
                    MAX(date_time) AS last_seen,
                    TIMESTAMPDIFF(SECOND, MAX(date_time), NOW()) AS age_seconds,
                    temperature,
                    humidity
                FROM weather
                WHERE sensor_id IN (1, 2, 3, 4, 5)
                GROUP BY sensor_id
                """
            )
            rows = cursor.fetchall()

            for sensor_id, last_seen, age_seconds, temperature, humidity in rows:
                statuses[sensor_id] = ("Connected", last_seen, temperature, humidity) if age_seconds <= timeout_seconds else ("Disconnected", last_seen, temperature, humidity)

            return statuses

    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return statuses

    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
