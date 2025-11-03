import streamlit as st
import sqlite3
import pandas as pd

# Page setup
st.set_page_config(
    page_title="Network Traffic Dashboard",
    page_icon="🌐",
    layout="wide",
)

st.title("🌐 Network Traffic Dashboard")
st.caption("Real-Time Packet Capture & Analysis (FYP Project)")

# Connect to SQLite and ensure table exists
conn = sqlite3.connect("packets.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS packets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    src_ip TEXT,
    dst_ip TEXT,
    protocol TEXT,
    size INTEGER,
    timestamp TEXT,
    threat_type TEXT,
    location TEXT
)
""")
conn.commit()

# Check if table is empty, insert sample data if so
df = pd.read_sql_query("SELECT * FROM packets", conn)
if df.empty:
    sample_packets = [
        ("192.168.1.2", "10.0.0.5", "TCP", 1500, "2025-11-03 12:00:00", "Normal", "Local"),
        ("192.168.1.3", "10.0.0.10", "UDP", 500, "2025-11-03 12:01:00", "Suspicious", "Local"),
        ("10.0.0.5", "192.168.1.2", "TCP", 1500, "2025-11-03 12:02:00", "SYN Flood", "Remote"),
        ("192.168.1.4", "10.0.0.15", "UDP", 800, "2025-11-03 12:03:00", "Malformed", "Remote"),
        ("10.0.0.10", "192.168.1.3", "TCP", 1200, "2025-11-03 12:04:00", "Normal", "Local"),
    ]
    cursor.executemany("""
    INSERT INTO packets (src_ip, dst_ip, protocol, size, timestamp, threat_type, location)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, sample_packets)
    conn.commit()
    df = pd.read_sql_query("SELECT * FROM packets", conn)

conn.close()

# Show a friendly message if empty (should not happen now)
if df.empty:
    st.warning("No packet data available yet. Please run capture or insert sample packets first.")
else:
    # Show metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Packets", len(df))
    col2.metric("Unique Source IPs", df["src_ip"].nunique())
    col3.metric("Unique Dest IPs", df["dst_ip"].nunique())

    # Tabs for analysis
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "📁 Raw Data", "🔍 Filters"])

    # Tab 1: Overview charts
    with tab1:
        st.subheader("Protocol Distribution")
        proto_count = df["protocol"].value_counts()
        st.bar_chart(proto_count)

        st.subheader("Top 10 Source IPs")
        top_src = df["src_ip"].value_counts().head(10)
        st.bar_chart(top_src)

    # Tab 2: Raw data
    with tab2:
        st.subheader("Captured Packets")
        st.dataframe(df, width='stretch')

    # Tab 3: Filtering
    with tab3:
        st.subheader("Filter by Protocol or IP")
        protocol = st.selectbox("Select Protocol", ["All"] + sorted(df["protocol"].unique().tolist()))
        ip_filter = st.text_input("Search by IP Address")

        filtered_df = df.copy()
        if protocol != "All":
            filtered_df = filtered_df[filtered_df["protocol"] == protocol]
        if ip_filter:
            filtered_df = filtered_df[(filtered_df["src_ip"].str.contains(ip_filter)) | 
                                      (filtered_df["dst_ip"].str.contains(ip_filter))]

        st.write(f"Showing {len(filtered_df)} packets")
        st.dataframe(filtered_df, width='stretch')
