import sqlite3

'''CRUD = Create, Read, Update, Delete'''

def initiate_db():
    connection = sqlite3.connect('database-products.db')
    cursor = connection.cursor()

    # создаем таблицу в БД, если ее нет:
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL,
    image TEXT NOT NULL
    )''')
    # сохраняем изменения и закрываем соединение с БД:
    connection.commit()
    connection.close()

def _fill_db():
    connection = sqlite3.connect('database-products.db')
    cursor = connection.cursor()
    # если пустая:
    for j in range(1, 5):
        cursor.execute('INSERT INTO Products (title, description, price, image) VALUES (?, ?, ?, ?)',
                       (f'Product-{j}', f'описание {j}', j*100, f'photo_{j}'))
    # сохраняем изменения и закрываем соединение с БД:
    connection.commit()
    connection.close()

def get_all_products():
    connection = sqlite3.connect('database-products.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    connection.close()
    return products

def print_db():
    connection = sqlite3.connect('database-products.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    col_names = [_[0] for _ in cursor.description]
    print(col_names)
    for p in products:
        print(p)
    connection.close()

if __name__ == '__main__':
    initiate_db()
    _fill_db()
    print_db()
