import streamlit as st
import yfinance as yf

st.title("📊 Analisa Saham V1")

ticker = st.text_input("Masukkan kode saham", "AAPL")
period = st.selectbox("Pilih periode", ["1mo", "3mo", "6mo", "1y"])

if st.button("Analisa"):
    data = yf.download(ticker, period=period)

    if data.empty:
        st.error("Data tidak ditemukan!")
    else:
        st.line_chart(data["Close"])

        last_price = data["Close"].iloc[-1]
        avg_price = data["Close"].mean()

        if last_price > avg_price:
            st.success("Trend: NAIK 📈")
        else:
            st.warning("Trend: TURUN 📉")

        st.write("Harga terakhir:", last_price)
        st.write("Rata-rata:", avg_price)
