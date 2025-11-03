import sqlite3

# Connect to the database
conn = sqlite3.connect("packets.db")
cursor = conn.cursor()

# Create a new packets table with the correct columns
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
conn.close()

print("New packets table created successfully.")
