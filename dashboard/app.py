import streamlit as st
import psycopg2
import pandas as pd
from prophet import Prophet

st.set_page_config(page_title="Bank Credit Target System", page_icon="🏦", layout="wide")
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
def get_forecast(_df_key, kanal, df):
    if kanal == "Ümumi Bank":
        kanal_df = df.groupby("ds")["y"].sum().reset_index()
    else:
        kanal_df = df[df["kanal"] == kanal][["ds", "y"]]
    model = Prophet()
    model.fit(kanal_df)
    future = model.make_future_dataframe(periods=6, freq="MS")
    forecast = model.predict(future)
    return forecast, kanal_df

df = load_data()

seçimlər = ["Ümumi Bank"] + list(df["kanal"].unique())
kanal = st.selectbox("Kanal seçin:", seçimlər)

forecast, kanal_df = get_forecast(kanal, kanal, df)

son_6 = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(6).copy()

# --- METRİK KARTLAR ---
st.subheader("📊 Növbəti ay proqnozu")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Proqnoz (AZN)", value=f"{son_6.iloc[0]['yhat']:,.0f}")
with col2:
    st.metric(label="Aşağı hədd", value=f"{son_6.iloc[0]['yhat_lower']:,.0f}")
with col3:
    st.metric(label="Yuxarı hədd", value=f"{son_6.iloc[0]['yhat_upper']:,.0f}")

# --- TREND QRAFİKİ ---
st.subheader("📈 Keçmiş trend və proqnoz")
chart_df = forecast[["ds", "yhat"]].copy()
chart_df.columns = ["Tarix", "Proqnoz"]
historical = kanal_df[["ds", "y"]].copy()
historical.columns = ["Tarix", "Həqiqi"]
merged = pd.merge(chart_df, historical, on="Tarix", how="left")
merged = merged.set_index("Tarix")
st.line_chart(merged)

# --- 6 AYLIK CƏDVƏL ---
st.subheader("📋 6 aylıq proqnoz cədvəli")
son_6.columns = ["Tarix", "Proqnoz (AZN)", "Aşağı hədd", "Yuxarı hədd"]
for col in ["Proqnoz (AZN)", "Aşağı hədd", "Yuxarı hədd"]:
    son_6[col] = son_6[col].apply(lambda x: f"{x:,.0f}")
son_6["Tarix"] = son_6["Tarix"].dt.strftime("%b %Y")
st.dataframe(son_6.set_index("Tarix"), width="stretch")

# --- KANAL MÜQAYİSƏ CƏDVƏLİ ---
st.subheader("🏦 Kanal üzrə müqayisə")
@st.cache_data
def get_all_forecasts(df):
    nəticə = []
    for k in df["kanal"].unique():
        k_df = df[df["kanal"] == k][["ds", "y"]]
        m = Prophet()
        m.fit(k_df)
        fut = m.make_future_dataframe(periods=1, freq="MS")
        fc = m.predict(fut)
        nəticə.append({"Kanal": k, "Növbəti ay proqnozu (AZN)": f"{fc['yhat'].iloc[-1]:,.0f}"})
    return pd.DataFrame(nəticə)

muqayise_df = get_all_forecasts(df)
st.dataframe(muqayise_df.set_index("Kanal"), width="stretch")