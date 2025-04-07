# api.py
from fastapi import FastAPI
import pymssql
from datetime import datetime
from dotenv import load_dotenv
import os
app = FastAPI()

# โหลด environment variables จาก .env
load_dotenv()
SERVER = os.getenv("SERVER")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")

_connection = pymssql.connect(server=SERVER, user=USER, password=PASSWORD, database=DATABASE)

def get_shift(time):
    hour = time.hour
    if 9 <= hour < 10:
        return "A"
    elif 10 <= hour < 11:
        return "B"
    elif 11 <= hour < 13:
        return "C"
    elif 13 <= hour < 24 or 0 <= hour < 9:
        return "D"
    return "Unknown"

@app.post("/add_data")
async def add_data(data: dict):
    current_time = datetime.now()
    shift = get_shift(current_time)
    with _connection.cursor() as cursor:
        cursor.execute("""
        MERGE user_data AS target
        USING (SELECT %s AS data_1) AS source
        ON (target.data_1 = source.data_1)
        WHEN MATCHED THEN
            UPDATE SET time = %s, shift = %s, data_2 = %s, data_3 = %s, data_4 = %s, data_5 = %s
        WHEN NOT MATCHED THEN
            INSERT (time, shift, data_1, data_2, data_3, data_4, data_5)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (data["data_1"], current_time, shift, data["data_2"], data["data_3"], data["data_4"], data["data_5"],
              current_time, shift, data["data_1"], data["data_2"], data["data_3"], data["data_4"], data["data_5"]))
        _connection.commit()
    return {"status": "success"}

@app.get("/get_data")
async def get_data(shift_option: str = "All"):
    with _connection.cursor() as cursor:
        if shift_option == "All":
            cursor.execute("""
                SELECT TOP 10 no, time, shift, data_1, data_2, data_3, data_4, data_5
                FROM user_data
                ORDER BY time DESC
            """)
        else:
            cursor.execute("""
                SELECT TOP 10 no, time, shift, data_1, data_2, data_3, data_4, data_5
                FROM user_data
                WHERE shift = %s
                ORDER BY time DESC
            """, (shift_option,))
        rows = cursor.fetchall()
    return {"data": [dict(zip(["no", "time", "shift", "data_1", "data_2", "data_3", "data_4", "data_5"], row)) for row in rows]}

# รันด้วย: uvicorn api:app --reload