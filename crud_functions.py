import sqlite3


def initiate_db():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Products (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    prise INTEGER NOT NULL
    )
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_title_index ON Products(title)")

    for i in range(1, 5):
        cursor.execute("INSERT INTO Products (title, description, prise) VALUES (?, ?, ?)",
                       (f"Product{i}",
                        f"Description{i}",
                        f"{i * 100}"))

    connection.commit()
    connection.close()


def get_all_products():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Products")

    products = cursor.fetchall()

    connection.commit()
    connection.close()

    return products


initiate_db()
print(get_all_products())
