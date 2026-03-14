# Bank Credit Target System

Azərbaycan bankı üçün aylıq kredit satış hədəfi proqnoz sistemi.

## Nə edir?
- PostgreSQL bazasında kanal və filial üzrə satış datası saxlayır
- Facebook Prophet modeli ilə növbəti 6 ay üçün proqnoz verir
- Streamlit dashboard ilə interaktiv vizuallaşdırma

## Texnologiyalar
- Python 3.11
- PostgreSQL
- Prophet (Meta)
- Streamlit
- Pandas

## İşə salmaq
```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
```
