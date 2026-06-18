import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Saham & Waran Final", layout="centered")

st.title("📊 Saham & Waran Analyzer FINAL")

# ================= INPUT =================
ticker = st.text_input("Kode Saham (BBCA.JK / AAPL)", "BBCA.JK")
mode = st.radio("Mode", ["Saham", "Waran"])

strike = 0
expiry = 0

if mode == "Waran":
    strike = st.number_input("Strike Price", value=100.0)
    expiry = st.number_input("Sisa Hari Expiry", value=90)

# ================= RUN =================
if st.button("ANALISA 🚀"):

    data = yf.download(ticker, period="3mo")

    if data.empty:
        st.error("Data tidak ditemukan. Cek ticker kamu.")
    else:

        close = data["Close"].dropna()
        last_price = float(close.iloc[-1])

        st.subheader("📈 Harga")
        st.line_chart(close)

        # ================= SAHAM LOGIC =================
        if mode == "Saham":

            avg = close.mean()

            if last_price > avg:
                st.success("📈 TREND NAIK (Bullish)")
            else:
                st.warning("📉 TREND TURUN (Bearish)")

            st.write("Harga terakhir:", last_price)
            st.write("Rata-rata:", avg)

        # ================= WARAN LOGIC =================
        else:

            status = "OTM"
            score = 0

            if last_price > strike:
                status = "ITM"
                score += 1
            else:
                score -= 1

            if expiry < 30:
                score -= 2
            elif expiry < 90:
                score -= 1

            st.write("Harga saham:", last_price)
            st.write("Strike:", strike)
            st.write("Expiry:", expiry)
            st.write("Status:", status)

            if score >= 1:
                st.success("🔥 WARAN MASIH MENARIK")
            else:
                st.error("⚠️ WARAN BERISIKO TINGGI")
