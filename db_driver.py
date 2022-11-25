import sqlite3

def initialize_db():
    db = sqlite3.connect('ddd_tracker.sqlite')

    # Create the tables if they don't exist
    # Event logger table, with user ID, and timestamp
    db.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Commit the changes
    db.commit()

def log_event(user_id):
    db = sqlite3.connect('ddd_tracker.sqlite')
    db.execute('INSERT INTO events (user_id) VALUES (?)', (user_id,))
    db.commit()

def get_events():
    db = sqlite3.connect('ddd_tracker.sqlite')

    # Return a list of tuples corresponding to the rows
    return db.execute('SELECT * FROM events').fetchall()