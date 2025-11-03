# fix_db.py
# Script to update or modify the database schema or data as needed.

import sqlite3
conn = sqlite3.connect("packets.db")
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS packets")
conn.commit()
conn.close()
print("Table dropped. Run your capture script to recreate it.")
