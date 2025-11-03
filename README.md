# NTAVis Project

**Network Traffic Analysis & Visualization (NTAVis)** is a real-time network monitoring tool that detects threats, visualizes network activity, and sends instant alerts.

## Features

- Real-time packet capture and analysis
- Threat detection (Malformed, UDP Flood, Suspicious, SYN Flood)
- Interactive dashboard for data visualization (Streamlit)
- Telegram alerts for detected threats
- Geo-mapping of threat sources
- Database management utilities

## Requirements

All Python dependencies are listed in `requirements.txt`.

Install them with:
```
pip install -r requirements.txt
```

## How to Use

1. **Capture Network Packets**
   - Run `capture.py` to capture live network packets and process them for analysis.

2. **Insert or Parse Data**
   - Use `insert_packets.py` to insert sample or real packet data (with geolocation) into the database.
   - Use `parse_and_save.py` to parse raw packet data and save it to the database.

3. **Database Management**
   - Run `clear_db.py` to clear all data from the packets database.
   - Use `fix_db.py` if you need to fix or update the database schema/data.

4. **Threat Alerts**
   - Configure your Telegram credentials in `NTAVis_bot.py` and run it to receive instant alerts for detected threats.

5. **Visualize Data**
   - Run `streamlit_dashboard.py` (or `app.py`/`dashboard.py`) to launch the interactive dashboard in your browser.

## Script Descriptions

- **capture.py**: Captures network packets for analysis.
- **insert_packets.py**: Inserts packet data with geolocation into the database.
- **parse_and_save.py**: Parses and saves packet data.
- **clear_db.py**: Clears all data from the packets database.
- **fix_db.py**: Fixes or updates the database schema/data.
- **NTAVis_bot.py**: Sends Telegram alerts for detected threats (configure your own TOKEN and CHAT_ID).
- **streamlit_dashboard.py**: Main dashboard for data visualization.
- **app.py**: Alternative dashboard scripts.

## Project Structure

- `app.py`: Project scripts
- `index.html`: Website landing page
- `requirements.txt`: Python dependencies
- `README.md`: Project documentation
- `LICENSE`: Usage terms

## Author

Muhammad Hadif Shah Bin Mohd Hadli Shah

## License

See the `LICENSE` file.  
This project is for Network Traffic Analsysis & Visualisation System Final Year Project.
