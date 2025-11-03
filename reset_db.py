import sqlite3

# Connect to your database
conn = sqlite3.connect("packets.db")
cursor = conn.cursor()

# Drop the old table
cursor.execute("DROP TABLE IF EXISTS packets")
conn.commit()
conn.close()

print("Old table dropped.")
