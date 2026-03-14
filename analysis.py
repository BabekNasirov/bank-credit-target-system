import psycopg2
import pandas as pd
conn = psycopg2.connect(
    host="localhost",
    database="bank_credit_db",
    user="babeknasirov",
    password=""
)
cur = conn.cursor()
cur.execute("""
    SELECT c.name as kanal, u.name as bolme,
           m.year as il, m.month as ay,
           m.target_azn as hedef,
           m.actual_azn as icra,
           m.achievement_pct as faiz
    FROM monthly_sales m
    JOIN units u ON m.unit_id = u.id
    JOIN channels c ON u.channel_id = c.id
    ORDER BY m.year, m.month, c.name
""")
df = pd.DataFrame(cur.fetchall(), columns=[desc[0] for desc in cur.description])
print(df.head(10))