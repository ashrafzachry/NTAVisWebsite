import sqlite3

# Database file
DB_PATH = "packets.db"

# Sample data
sample_packets = [
    ("192.168.1.2", "10.0.0.5", "TCP", 1500, "2025-11-03 12:00:00", "Normal"),
    ("192.168.1.3", "10.0.0.10", "UDP", 500, "2025-11-03 12:01:00", "Suspicious"),
    ("10.0.0.5", "192.168.1.2", "TCP", 1500, "2025-11-03 12:02:00", "SYN Flood"),
    ("192.168.1.4", "10.0.0.15", "UDP", 800, "2025-11-03 12:03:00", "Malformed"),
    ("10.0.0.10", "192.168.1.3", "TCP", 1200, "2025-11-03 12:04:00", "Normal"),
]

# Connect to SQLite and create table
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

# Insert sample data
cursor.executemany("""
INSERT INTO packets (src_ip, dst_ip, protocol, size, timestamp, threat_type)
VALUES (?, ?, ?, ?, ?, ?)
""", sample_packets)
conn.commit()
conn.close()

print(f"Sample database created at {DB_PATH} with {len(sample_packets)} packets.")
