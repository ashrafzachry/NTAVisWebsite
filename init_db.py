import sqlite3

# Connect to the database (creates the file if it doesn't exist)
conn = sqlite3.connect("packets.db")
cursor = conn.cursor()

# Create the table if it doesn't exist
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
conn.close()

print("✅ packets table created successfully!")
