import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Smart Analyzer FINAL", layout="centered")

st.title("📊 Smart Stock & Waran Analyzer FINAL")
st.write("Analisa sederhana: trend, RSI, MA, dan risiko waran")

# ================= INPUT =================
ticker = st.text_input("Kode Saham / Waran", "AAPL")
period = st.selectbox("Periode", ["1mo", "3mo", "6mo", "1y"])
mode = st.radio("Mode", ["Saham", "Waran"])

strike = 0
expiry = 0

if mode == "Waran":
    strike = st.number_input("Strike Price", value=100.0)
    expiry = st.number_input("Sisa Hari Expiry", value=90)

# ================= RSI =================
def rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# ================= RUN =================
if st.button("ANALISA 🚀"):

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
