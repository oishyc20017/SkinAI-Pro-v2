from database.db import get_connection


def create_tables():

    conn = get_connection()
    c = conn.cursor()

    # =========================
    # Users
    # =========================

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TEXT
    )
    """)

    # =========================
    # Prediction History
    # =========================

    c.execute("""
    CREATE TABLE IF NOT EXISTS prediction_history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        disease TEXT NOT NULL,
        confidence REAL NOT NULL,
        image_path TEXT,
        created_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # =========================
    # Conversations
    # =========================

    c.execute("""
    CREATE TABLE IF NOT EXISTS conversations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT,
        created_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # =========================
    # Messages
    # =========================

    c.execute("""
    CREATE TABLE IF NOT EXISTS messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        role TEXT NOT NULL,
        message TEXT NOT NULL,
        created_at TEXT,
        FOREIGN KEY(conversation_id) REFERENCES conversations(id),
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # =========================
    # Doctor Bookings
    # =========================

    c.execute("""
    CREATE TABLE IF NOT EXISTS bookings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,

        doctor_name TEXT NOT NULL,
        specialty TEXT,
        hospital_name TEXT,

        patient_name TEXT,
        patient_email TEXT,
        phone TEXT,

        booking_date TEXT NOT NULL,
        booking_time TEXT NOT NULL,

        symptoms TEXT,
        payment_method TEXT,

        status TEXT DEFAULT 'Pending',

        created_at TEXT,

        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # =========================
    # Existing booking columns
    # =========================

    c.execute("PRAGMA table_info(bookings)")

    existing_columns = [
        row[1]
        for row in c.fetchall()
    ]

    new_columns = {
        "patient_name": "TEXT",
        "patient_email": "TEXT",
        "phone": "TEXT",
        "specialty": "TEXT",
        "hospital_name": "TEXT",
        "symptoms": "TEXT",
        "payment_method": "TEXT"
    }

    for column_name, column_type in new_columns.items():

        if column_name not in existing_columns:

            c.execute(
                f"""
                ALTER TABLE bookings
                ADD COLUMN {column_name} {column_type}
                """
            )

    conn.commit()
    conn.close()