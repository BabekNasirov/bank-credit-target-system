# Bank Credit Target System

🇦🇿 **Azərbaycanca** | 🇬🇧 **English**

---

## 🇦🇿 Azərbaycanca

Azərbaycan bankı üçün aylıq kredit satış hədəfi proqnoz sistemi.

### Nə edir?
- PostgreSQL bazasında kanal və filial üzrə satış datası saxlayır
- Facebook Prophet modeli ilə növbəti 6 ay üçün proqnoz verir
- Streamlit dashboard ilə interaktiv vizuallaşdırma
- Bütün kanallar üzrə müqayisə və metrik kartlar

### Texnologiyalar
- Python 3.11
- PostgreSQL
- Prophet (Meta)
- Streamlit
- Pandas

### İşə salmaq
```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
```

---

## 🇬🇧 English

A monthly credit sales target forecasting system for an Azerbaijani bank.

### What does it do?
- Stores sales data by channel and branch in a PostgreSQL database
- Forecasts the next 6 months using Facebook Prophet
- Interactive visualization with a Streamlit dashboard
- Channel comparison and metric cards

### Technologies
- Python 3.11
- PostgreSQL
- Prophet (Meta)
- Streamlit
- Pandas

### How to run
```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
```
