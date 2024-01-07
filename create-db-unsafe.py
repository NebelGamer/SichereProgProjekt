import sqlite3

# Verbindung zur Datenbank herstellen (falls nicht vorhanden, wird eine neue Datenbank erstellt)
connection = sqlite3.connect("unsafe-test.db")

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

# Unsicher: Direkte Verwendung von Benutzereingaben in der SQL-Abfrage
username = input("Bitte geben Sie den Benutzernamen ein: ")
password = input("Bitte geben Sie das Passwort ein: ")

# Unsicher: Direkte Verwendung von Benutzereingaben in der SQL-Abfrage
cursor.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")

# Änderungen bestätigen und Verbindung schließen
connection.commit()
connection.close()
