import streamlit as st
import psycopg2
import pandas as pd
from prophet import Prophet

st.title("🏦 Bank Credit Target System")
st.subheader("Aylıq satış hədəfi proqnozu")

@st.cache_data
def load_data():
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
    cur.close()
    conn.close()
    df["ds"] = pd.to_datetime(df["year"].astype(str) + "-" + df["month"].astype(str) + "-01")
    df["y"] = df["umumi_icra"]
    return df

@st.cache_data
def get_forecast(kanal, df):
    if kanal == "Ümumi Bank":
        kanal_df = df.groupby("ds")["y"].sum().reset_index()
    else:
        kanal_df = df[df["kanal"] == kanal][["ds", "y"]]
    model = Prophet()
    model.fit(kanal_df)
    future = model.make_future_dataframe(periods=6, freq="MS")
    forecast = model.predict(future)
    return forecast

df = load_data()

seçimlər = ["Ümumi Bank"] + list(df["kanal"].unique())
kanal = st.selectbox("Kanal seçin:", seçimlər)

forecast = get_forecast(kanal, df)

st.subheader(f"{kanal} — növbəti 6 ay proqnozu")

son_6 = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(6).copy()
son_6.columns = ["Tarix", "Proqnoz (AZN)", "Aşağı hədd", "Yuxarı hədd"]
for col in ["Proqnoz (AZN)", "Aşağı hədd", "Yuxarı hədd"]:
    son_6[col] = son_6[col].apply(lambda x: f"{x:,.0f}")
son_6["Tarix"] = son_6["Tarix"].dt.strftime("%b %Y")

st.dataframe(son_6.set_index("Tarix"), width="stretch")

st.subheader("Proqnoz qrafiki")
st.line_chart(forecast.set_index("ds")["yhat"])