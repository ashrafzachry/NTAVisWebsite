import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd

st.set_page_config(page_title="NTAVis Project", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "landing"

# Landing page HTML
landing_html = """
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container">
    <a class="navbar-brand" href="#">NTAVis</a>
    <div class="collapse navbar-collapse">
      <ul class="navbar-nav ms-auto">
        <li class="nav-item"><a class="nav-link" href="#">Home</a></li>
        <li class="nav-item"><a class="nav-link" href="#about">About</a></li>
        <li class="nav-item"><a class="nav-link" href="#features">Features</a></li>
        <li class="nav-item"><a class="nav-link" href="#contact">Contact</a></li>
      </ul>
    </div>
  </div>
</nav>
<header class="bg-primary text-white text-center py-5">
  <div class="container">
    <h1>Network Traffic Analysis & Visualization (NTAVis)</h1>
    <p class="lead">Real-time threat detection, visualization, and alerting system</p>
    <button id="goDashboard">Go to Dashboard</button>
  </div>
</header>
<section id="about" class="py-5">
  <div class="container">
    <h2>About the Project</h2>
    <p>
      NTAVis is a real-time network traffic analysis and visualization tool that detects threats using an Intrusion Detection System (IDS) and sends instant alerts via Telegram. It captures network packets, analyzes them for suspicious activity, and displays results on an interactive dashboard.
    </p>
  </div>
</section>
<section id="features" class="py-5 bg-light">
  <div class="container">
    <h2>Features</h2>
    <ul>
      <li>Real-time packet capture and analysis</li>
      <li>Threat detection (Malformed, UDP Flood, Suspicious, SYN Flood)</li>
      <li>Interactive dashboard for data visualization</li>
      <li>Instant Telegram alerts for detected threats</li>
      <li>Geo-mapping of threat sources</li>
    </ul>
  </div>
</section>
<section id="contact" class="py-5">
  <div class="container">
    <h2>Contact</h2>
    <p>For more information, contact: <a href="mailto:hadifshah177@gmail.com">hadifshah177@gmail.com</a></p>
  </div>
</section>
<footer class="bg-dark text-white text-center py-3">
  <div class="container">
    &copy; 2025 NTAVis Project
  </div>
</footer>
"""

# Instead of rerun, use a selectbox for navigation
page = st.selectbox("Navigation", ["Landing Page", "Dashboard"], index=0 if st.session_state.page=="landing" else 1)
st.session_state.page = page

if st.session_state.page == "landing":
    components.html(landing_html, height=1000, scrolling=True)

elif st.session_state.page == "Dashboard":
    st.title("🌐 Network Traffic Dashboard")
    st.caption("Real-Time Packet Capture & Analysis (FYP Project)")

    DB_PATH = "packets.db"
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query("SELECT * FROM packets", conn)
    except Exception:
        df = pd.DataFrame(columns=["id","src_ip","dst_ip","protocol","size","timestamp","threat_type"])
    conn.close()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Packets", len(df))
    col2.metric("Unique Source IPs", df["src_ip"].nunique())
    col3.metric("Unique Dest IPs", df["dst_ip"].nunique())

    tab1, tab2, tab3 = st.tabs(["📊 Overview", "📁 Raw Data", "🔍 Filters"])
    with tab1:
        st.subheader("Protocol Distribution")
        st.bar_chart(df["protocol"].value_counts())
        st.subheader("Top 10 Source IPs")
        st.bar_chart(df["src_ip"].value_counts().head(10))
    with tab2:
        st.subheader("Captured Packets")
        st.dataframe(df, use_container_width=True)
    with tab3:
        st.subheader("Filter by Protocol or IP")
        protocol = st.selectbox("Select Protocol", ["All"] + sorted(df["protocol"].unique().tolist()))
        ip_filter = st.text_input("Search by IP Address")
        filtered_df = df.copy()
        if protocol != "All":
            filtered_df = filtered_df[filtered_df["protocol"] == protocol]
        if ip_filter:
            filtered_df = filtered_df[(df["src_ip"].str.contains(ip_filter)) | 
                                      (df["dst_ip"].str.contains(ip_filter))]
        st.write(f"Showing {len(filtered_df)} packets")
        st.dataframe(filtered_df, use_container_width=True)
