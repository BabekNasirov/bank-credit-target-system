import psycopg2
import numpy as np
from datetime import datetime

np.random.seed(42)

SEASONALITY = {
    1: 0.85, 2: 0.88, 3: 0.95, 4: 1.05,
    5: 1.10, 6: 1.08, 7: 0.92, 8: 0.90,
    9: 1.02, 10: 1.05, 11: 1.12, 12: 1.18
}

conn = psycopg2.connect(
    host="localhost",
    database="bank_credit_db",
    user="babeknasirov",
    password=""
)
cur = conn.cursor()

# Bütün unit-ləri və base_target-ləri çək
cur.execute("""
    SELECT u.id, u.name, c.base_target
    FROM units u
    JOIN channels c ON u.channel_id = c.id
""")
units = cur.fetchall()

records = []
for year in range(2022, 2025):
    for month in range(1, 13):
        if year == 2024 and month > datetime.now().month:
            break
        for unit_id, unit_name, base_target in units:
            trend = 1 + (year - 2022) * 0.08
            season = SEASONALITY[month]
            noise = np.random.uniform(0.85, 1.15)

            actual = round(float(base_target) * trend * season * noise, 2)
            target = round(float(base_target) * trend * season * 0.95, 2)
            achievement = round((actual / target) * 100, 1)

            records.append((unit_id, year, month, target, actual, achievement))

cur.executemany("""
    INSERT INTO monthly_sales (unit_id, year, month, target_azn, actual_azn, achievement_pct)
    VALUES (%s, %s, %s, %s, %s, %s)
""", records)

conn.commit()
cur.close()
conn.close()

print(f"{len(records)} sətir data bazaya yazıldı!")