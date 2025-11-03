# streamlit_app.py
import streamlit as st
import sqlite3
import pandas as pd
import os

# ---------------------------
# CONFIG
# ---------------------------
DB_PATH = "packets.db"  # SQLite DB in current directory

st.set_page_config(
    page_title="Network Traffic Dashboard",
    page_icon="🌐",
    layout="wide",
)

st.title("🌐 Network Traffic Dashboard")
st.caption("Real-Time Packet Capture & Analysis (FYP Project)")

# ---------------------------
# DATABASE SETUP
# ---------------------------
# Ensure DB exists and table is created
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS packets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    src_ip TEXT,
    dst_ip TEXT,
    protocol TEXT,
    size INTEGER,
    timestamp TEXT,
    threat_type TEXT
)
""")
conn.commit()

# ---------------------------
# LOAD DATA SAFELY
# ---------------------------
try:
    df = pd.read_sql_query("SELECT * FROM packets", conn)
except Exception as e:
    st.error(f"Database error: {e}")
    df = pd.DataFrame(columns=["id","src_ip","dst_ip","protocol","size","timestamp","threat_type"])

conn.close()

# ---------------------------
# DASHBOARD LOGIC
# ---------------------------
if df.empty:
    st.warning(
        "No packet data available yet. "
        "You can run `capture.py` or `insert_packets.py` locally to add sample data."
    )
else:
    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Packets", len(df))
    col2.metric("Unique Source IPs", df["src_ip"].nunique())
    col3.metric("Unique Dest IPs", df["dst_ip"].nunique())

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "📁 Raw Data", "🔍 Filters"])

    # ---------------------------
    # Tab 1: Overview
    # ---------------------------
    with tab1:
        st.subheader("Protocol Distribution")
        proto_count = df["protocol"].value_counts()
        st.bar_chart(proto_count)

        st.subheader("Top 10 Source IPs")
        top_src = df["src_ip"].value_counts().head(10)
        st.bar_chart(top_src)

    # ---------------------------
    # Tab 2: Raw Data
    # ---------------------------
    with tab2:
        st.subheader("Captured Packets")
        st.dataframe(df, use_container_width=True)

    # ---------------------------
    # Tab 3: Filtering
    # ---------------------------
    with tab3:
        st.subheader("Filter by Protocol or IP")
        protocol = st.selectbox(
            "Select Protocol", ["All"] + sorted(df["protocol"].dropna().unique().tolist())
        )
        ip_filter = st.text_input("Search by IP Address")

        filtered_df = df.copy()
        if protocol != "All":
            filtered_df = filtered_df[filtered_df["protocol"] == protocol]
        if ip_filter:
            filtered_df = filtered_df[
                (filtered_df["src_ip"].str.contains(ip_filter)) |
                (filtered_df["dst_ip"].str.contains(ip_filter))
            ]

        st.write(f"Showing {len(filtered_df)} packets")
        st.dataframe(filtered_df, use_container_width=True)
