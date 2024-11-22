import sqlite3

def connect_db():
    return sqlite3.connect("students.db")

def setup_database():
    conn = connect_db()
    cursor = conn.cursor()

    # Tạo bảng người dùng (users)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Tạo bảng sinh viên (students)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    """)

    # Thêm dữ liệu mẫu
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("admin", "admin123"))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
