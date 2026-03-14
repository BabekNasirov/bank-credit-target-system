import psycopg2
import pandas as pd
from prophet import Prophet

conn = psycopg2.connect(
    host="localhost",
    database="bank_credit_db",
    user="babeknasirov",
    password=""
)
cur = conn.cursor()

cur.execute("""
    SELECT m.year, m.month, c.name as kanal,
           SUM(m.actual_azn) as umumi_icra
    FROM monthly_sales m
    JOIN units u ON m.unit_id = u.id
    JOIN channels c ON u.channel_id = c.id
    GROUP BY m.year, m.month, c.name
    ORDER BY m.year, m.month
""")

df = pd.DataFrame(cur.fetchall(), columns=[desc[0] for desc in cur.description])
df["ds"] = pd.to_datetime(df["year"].astype(str) + "-" + df["month"].astype(str) + "-01")
df["y"] = df["umumi_icra"]

kanallar = df["kanal"].unique()
umumi_proqnoz = {}

for kanal in kanallar:
    kanal_df = df[df["kanal"] == kanal][["ds", "y"]]
    model = Prophet()
    model.fit(kanal_df)
    future = model.make_future_dataframe(periods=6, freq="MS")
    forecast = model.predict(future)
    forecast["yhat_rounded"] = forecast["yhat"].round(2)
    print(f"\n{kanal} kanalı üçün proqnoz (AZN):")
    print(forecast[["ds", "yhat_rounded"]].tail(6).to_string(index=False))
    umumi_proqnoz[kanal] = forecast[["ds", "yhat_rounded"]].tail(6)

umumi_df = pd.concat(umumi_proqnoz.values())
umumi_df = umumi_df.groupby("ds")["yhat_rounded"].sum().reset_index()
print("\n--- ÜMUMİ BANK ÜZRƏ PROQNOZ (AZN) ---")
print(umumi_df.to_string(index=False))

cur.close()
conn.close()