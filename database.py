import sqlite3

DATABASE = "college.db"

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Students Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        roll TEXT UNIQUE,
        branch TEXT,
        year INTEGER,
        phone TEXT,
        email TEXT,
        cgpa REAL
    )
    """)

    # Faculty Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS faculty(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        faculty_id TEXT UNIQUE,
        department TEXT,
        qualification TEXT,
        experience INTEGER,
        phone TEXT,
        email TEXT
    )
    """)

    # Attendance Table
    cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll TEXT UNIQUE,
    branch TEXT,
    year INTEGER,
    phone TEXT,
    email TEXT,
    cgpa REAL,
    attendance REAL,
    marks REAL
)
""")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database Created Successfully")