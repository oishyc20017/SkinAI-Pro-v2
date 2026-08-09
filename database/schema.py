from database.db import get_connection, get_database_backend


def create_tables():

    conn = get_connection()

    backend = get_database_backend()

    try:

        # =========================================
        # SQLITE
        # =========================================

        if backend == "sqlite":

            c = conn.cursor()

            # Users
            c.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fullname TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    created_at TEXT
                )
            """)

            # Prediction History
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

            # Conversations
            c.execute("""
                CREATE TABLE IF NOT EXISTS conversations(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title TEXT,
                    created_at TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            """)

            # Messages
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

            # Doctor Bookings
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

            conn.commit()
            c.close()

        # =========================================
        # NEON POSTGRESQL
        # =========================================

        elif backend == "neon":

            with conn.cursor() as c:

                # Users
                c.execute("""
                    CREATE TABLE IF NOT EXISTS users(
                        id SERIAL PRIMARY KEY,
                        fullname TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        created_at TEXT
                    )
                """)

                # Prediction History
                c.execute("""
                    CREATE TABLE IF NOT EXISTS prediction_history(
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL,
                        disease TEXT NOT NULL,
                        confidence DOUBLE PRECISION NOT NULL,
                        image_path TEXT,
                        created_at TEXT,
                        FOREIGN KEY(user_id) REFERENCES users(id)
                    )
                """)

                # Conversations
                c.execute("""
                    CREATE TABLE IF NOT EXISTS conversations(
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL,
                        title TEXT,
                        created_at TEXT,
                        FOREIGN KEY(user_id) REFERENCES users(id)
                    )
                """)

                # Messages
                c.execute("""
                    CREATE TABLE IF NOT EXISTS messages(
                        id SERIAL PRIMARY KEY,
                        conversation_id INTEGER NOT NULL,
                        user_id INTEGER NOT NULL,
                        role TEXT NOT NULL,
                        message TEXT NOT NULL,
                        created_at TEXT,
                        FOREIGN KEY(conversation_id) REFERENCES conversations(id),
                        FOREIGN KEY(user_id) REFERENCES users(id)
                    )
                """)

                # Doctor Bookings
                c.execute("""
                    CREATE TABLE IF NOT EXISTS bookings(
                        id SERIAL PRIMARY KEY,
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

            conn.commit()

        else:

            raise RuntimeError(
                f"Unsupported DATABASE_BACKEND: {backend}"
            )

    except Exception:

        conn.rollback()
        raise

    finally:

        conn.close()