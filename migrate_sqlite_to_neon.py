import sqlite3
import shutil
from pathlib import Path

import psycopg
import streamlit as st


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
SQLITE_DB = BASE_DIR / "skinai.db"
BACKUP_DB = BASE_DIR / "skinai_before_neon_migration.db"


# =========================================================
# CHECK SQLITE
# =========================================================

if not SQLITE_DB.exists():
    raise FileNotFoundError(
        f"SQLite database not found: {SQLITE_DB}"
    )


# =========================================================
# BACKUP SQLITE
# =========================================================

print("Creating SQLite backup...")

shutil.copy2(
    SQLITE_DB,
    BACKUP_DB
)

print(f"Backup created: {BACKUP_DB}")


# =========================================================
# SQLITE CONNECTION
# =========================================================

sqlite_conn = sqlite3.connect(
    str(SQLITE_DB)
)

sqlite_conn.row_factory = sqlite3.Row


# =========================================================
# NEON CONNECTION
# =========================================================

database_url = st.secrets.get(
    "NEON_DATABASE_URL"
)

if not database_url:
    sqlite_conn.close()

    raise RuntimeError(
        "NEON_DATABASE_URL is not configured."
    )


print("Connecting to Neon...")

neon_conn = psycopg.connect(
    database_url
)

print("Neon connected successfully.")


# =========================================================
# READ SQLITE DATA
# =========================================================

tables = [
    "users",
    "conversations",
    "messages",
    "prediction_history",
    "bookings"
]


data = {}

for table in tables:

    rows = sqlite_conn.execute(
        f"SELECT * FROM {table}"
    ).fetchall()

    data[table] = rows

    print(
        f"SQLite {table}: {len(rows)} rows"
    )


# =========================================================
# CHECK NEON
# =========================================================

print("\nChecking existing Neon data...")

neon_counts = {}

with neon_conn.cursor() as c:

    for table in tables:

        c.execute(
            f"SELECT COUNT(*) FROM {table}"
        )

        count = c.fetchone()[0]

        neon_counts[table] = count

        print(
            f"Neon {table}: {count} rows"
        )


# =========================================================
# SAFETY CHECK
# =========================================================

if any(
    count > 0
    for count in neon_counts.values()
):

    sqlite_conn.close()
    neon_conn.close()

    raise RuntimeError(
        "\nSTOP: Neon already contains data.\n"
        "No migration was performed.\n"
        "This prevents duplicate records."
    )


# =========================================================
# MIGRATION
# =========================================================

print("\nStarting migration...")


try:

    with neon_conn.cursor() as c:

        # =================================================
        # USERS
        # =================================================

        for row in data["users"]:

            c.execute(
                """
                INSERT INTO users(
                    id,
                    fullname,
                    email,
                    password,
                    created_at
                )
                VALUES(
                    %s, %s, %s, %s, %s
                )
                """,
                (
                    row["id"],
                    row["fullname"],
                    row["email"],
                    row["password"],
                    row["created_at"]
                )
            )


        # =================================================
        # CONVERSATIONS
        # =================================================

        for row in data["conversations"]:

            c.execute(
                """
                INSERT INTO conversations(
                    id,
                    user_id,
                    title,
                    created_at
                )
                VALUES(
                    %s, %s, %s, %s
                )
                """,
                (
                    row["id"],
                    row["user_id"],
                    row["title"],
                    row["created_at"]
                )
            )


        # =================================================
        # MESSAGES
        # =================================================

        for row in data["messages"]:

            c.execute(
                """
                INSERT INTO messages(
                    id,
                    conversation_id,
                    user_id,
                    role,
                    message,
                    created_at
                )
                VALUES(
                    %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    row["id"],
                    row["conversation_id"],
                    row["user_id"],
                    row["role"],
                    row["message"],
                    row["created_at"]
                )
            )


        # =================================================
        # PREDICTION HISTORY
        # =================================================

        for row in data["prediction_history"]:

            c.execute(
                """
                INSERT INTO prediction_history(
                    id,
                    user_id,
                    disease,
                    confidence,
                    image_path,
                    created_at
                )
                VALUES(
                    %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    row["id"],
                    row["user_id"],
                    row["disease"],
                    row["confidence"],
                    row["image_path"],
                    row["created_at"]
                )
            )


        # =================================================
        # BOOKINGS
        # =================================================

        for row in data["bookings"]:

            c.execute(
                """
                INSERT INTO bookings(
                    id,
                    user_id,
                    doctor_name,
                    booking_date,
                    booking_time,
                    status,
                    created_at,
                    patient_name,
                    patient_email,
                    phone,
                    specialty,
                    hospital_name,
                    symptoms,
                    payment_method
                )
                VALUES(
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    row["id"],
                    row["user_id"],
                    row["doctor_name"],
                    row["booking_date"],
                    row["booking_time"],
                    row["status"],
                    row["created_at"],
                    row["patient_name"],
                    row["patient_email"],
                    row["phone"],
                    row["specialty"],
                    row["hospital_name"],
                    row["symptoms"],
                    row["payment_method"]
                )
            )


    # =====================================================
    # RESET POSTGRES SEQUENCES
    # =====================================================

    sequence_tables = [
        "users",
        "conversations",
        "messages",
        "prediction_history",
        "bookings"
    ]

    for table in sequence_tables:

        c.execute(
            f"""
            SELECT setval(
                pg_get_serial_sequence(
                    '{table}',
                    'id'
                ),
                COALESCE(
                    (SELECT MAX(id) FROM {table}),
                    1
                ),
                true
            )
            """
        )


    # =====================================================
    # COMMIT
    # =====================================================

    neon_conn.commit()

    print("\nMigration committed successfully.")


except Exception:

    neon_conn.rollback()

    print(
        "\nMigration failed."
    )

    print(
        "Neon transaction rolled back."
    )

    raise


finally:

    sqlite_conn.close()
    neon_conn.close()


# =========================================================
# FINAL VERIFICATION
# =========================================================

print("\nMigration completed.")
print("SQLite backup is available at:")
print(BACKUP_DB)

print("\nExpected Neon counts:")

for table in tables:

    print(
        f"{table}: {len(data[table])}"
    )