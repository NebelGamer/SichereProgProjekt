import sqlite3

# Verbindung zur Datenbank herstellen (falls nicht vorhanden, wird eine neue Datenbank erstellt)
connection = sqlite3.connect("test.db")

# Cursor-Objekt erstellen
cursor = connection.cursor()

# Tabelle erstellen (falls noch nicht vorhanden)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

# Beispielbenutzer hinzufügen (ersetze dies durch sichere Methoden in einer Produktionsumgebung)
cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "admin"))
cursor.execute("INSERT INTO users (username, password) VALUES (?,?)", ("christian", "password"))
cursor.execute("INSERT INTO users (username, password) VALUES(?,?)", ("omar", "ramo"))

# Änderungen bestätigen und Verbindung schließen
connection.commit()
connection.close()
