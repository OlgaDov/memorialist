import sqlite3

connection = sqlite3.connect("cards.db")
cursor = connection.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    front TEXT NOT NULL,
    back TEXT NOT NULL,
    learned INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
""")

connection.commit()
connection.close()

print("✅ Database created successfully!")
