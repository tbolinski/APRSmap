import sqlite3

def create_db():
    connection = sqlite3.connect("packets.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS APRS_packets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        destination TEXT,
        latitude REAL,
        longitude REAL,
        altitude REAL,
        timestamp TEXT,
        comment TEXT,
        path TEXT)""")
    connection.commit()
    connection.close()

def store(data: {}):
    connection = sqlite3.connect("packets.db")
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO APRS_packets (
        source, destination, latitude, longitude, altitude, timestamp, comment, path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (data["source"], data["destination"], data["latitude"], data["longitude"], data["altitude"], data["timestamp"], data["comment"], data["path"]))
    connection.commit()
    connection.close()