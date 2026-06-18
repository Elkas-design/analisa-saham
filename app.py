import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Smart Analyzer STABLE", layout="centered")

st.title("📊 Smart Analyzer STABLE (Anti Error)")
st.write("Saham + Waran Analyzer versi stabil")

# ================= INPUT =================
st.subheader("🔎 Pilih Saham")

stock_list = [
    "BBCA.JK",
    "BMRI.JK",
    "BBRI.JK",
    "BRMS.JK",
    "GOTO.JK",
    "AAPL",
    "TSLA",
    "NVDA"
]

ticker = st.selectbox("Cari / pilih saham", stock_list)
period = st.selectbox("Periode", ["1mo", "3mo", "6mo", "1y"])
mode = st.radio("Mode", ["Saham", "Waran"])

strike = 0
expiry = 0

if mode == "Waran":
    strike = st.number_input("Strike Price", value=100.0)
    expiry = st.number_input("Sisa Hari Expiry", value=90)

# ================= AUTO TICKER FIX =================
if raw.isalpha() and len(raw) <= 5:
    ticker = raw.upper() + ".JK"
else:
    ticker = raw.upper()

# ================= RSI =================
def rsi(series, period=14):
    delta = series.diff()

    gain = delta.where(delta > 0, 0).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

# ================= RUN =================
if st.button("ANALISA 🚀"):

    data = yf.download(ticker, period=period)

    if data is None or data.empty:
        st.error("❌ Data tidak ditemukan. Coba ticker lain (contoh: BBCA, BBCA.JK, AAPL)")
    else:

        # CLEAN DATA (INI PENTING)
        data = data.dropna()

        close = data["Close"]

        # INDICATORS
        data["MA20"] = close.rolling(20).mean()
        data["MA50"] = close.rolling(50).mean()
        data["RSI"] = rsi(close)

        last_price = float(close.iloc[-1])
        rsi_val = float(data["RSI"].iloc[-1])

        ma20 = float(data["MA20"].iloc[-1])
        ma50 = float(data["MA50"].iloc[-1])

        # ================= CHART (STABIL) =================
        st.subheader("📈 Harga")
        st.line_chart(close)

        st.subheader("📊 RSI")
        st.line_chart(data["RSI"])

        # ================= SCORE SYSTEM =================
        score = 0

        if last_price > ma20:
            score += 1
        if ma20 > ma50:
            score += 1
        if rsi_val < 30:
            score += 1
        if rsi_val > 70:
            score -= 1

        # ================= WARAN =================
        if mode == "Waran":
            if last_price > strike:
                score += 1
                waran_status = "ITM"
            else:
                score -= 1
                waran_status = "OTM"

            if expiry < 30:
                score -= 2
            elif expiry < 90:
                score -= 1

        # ================= RESULT =================
        st.subheader("📌 HASIL")

        if score >= 3:
            st.success("🔥 STRONG BUY")
        elif score == 2:
            st.info("📈 BUY / ACCUMULATE")
        elif score == 1:
            st.warning("⚖️ NEUTRAL")
        else:
            st.error("📉 SELL / HIGH RISK")

        # ================= INFO =================
        st.write("Ticker:", ticker)
        st.write("Harga:", last_price)
        st.write("RSI:", rsi_val)
        st.write("Score:", score)

        if mode == "Waran":
            st.write("Status Waran:", waran_status)
            st.write("Strike:", strike)
            st.write("Expiry:", expiry)
    data = yf.download(ticker, period=period)

    if data.empty:
        st.error("Data tidak ditemukan")
    else:
        close = data["Close"]

        # indikator
        data["MA20"] = close.rolling(20).mean()
        data["MA50"] = close.rolling(50).mean()
        data["RSI"] = rsi(close)

        last_price = close.iloc[-1]
        rsi_val = data["RSI"].iloc[-1]
        ma20 = data["MA20"].iloc[-1]
        ma50 = data["MA50"].iloc[-1]

        # chart
        st.subheader("📈 Chart")
        st.line_chart(data[["Close", "MA20", "MA50"]])

        st.subheader("📊 RSI")
        st.line_chart(data["RSI"])

        # ================= SCORE =================
        score = 0

        # trend
        if last_price > ma20:
            score += 1
        if ma20 > ma50:
            score += 1

        # momentum
        if rsi_val < 30:
            score += 1
        if rsi_val > 70:
            score -= 1

        # ================= WARAN LOGIC =================
        waran_status = None

        if mode == "Waran":
            if last_price > strike:
                waran_status = "ITM (Aktif)"
                score += 1
            else:
                waran_status = "OTM (Belum aktif)"
                score -= 1

            if expiry < 30:
                score -= 2
            elif expiry < 90:
                score -= 1

        # ================= RESULT =================
        st.subheader("📌 HASIL ANALISA")

        if score >= 3:
            st.success("🔥 STRONG BUY")
        elif score == 2:
            st.info("📈 BUY / ACCUMULATE")
        elif score == 1:
            st.warning("⚖️ NEUTRAL")
        else:
            st.error("📉 SELL / HIGH RISK")

        # ================= DETAIL =================
        st.write("Harga terakhir:", last_price)
        st.write("RSI:", rsi_val)
        st.write("Score:", score)

        if mode == "Waran":
            st.write("Status Waran:", waran_status)
            st.write("Strike:", strike)
            st.write("Expiry:", expiry)
