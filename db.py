import sqlite3
#import random

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

'''Пример "CRUD" = Create, Read, Update, Delete'''
# SELECT FROM, WHERE, GROUP BY, HAVING, ORDER BY...

# создаем таблицу в БД, если ее нет:
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER
)
''')

# создадим Индекс (Индекс — это специальная структура, которая ускоряет поиск данных в БД):
cursor.execute('CREATE INDEX IF NOT EXISTS idx_email ON Users (email)')

# Создаем / вставляем:
'''
cursor.execute('INSERT INTO Users (username, email, age) VALUES (?, ?, ?)', ('Neuser', 'some@jmail.by', 39))
for j in range(10):
    cursor.execute('INSERT INTO Users (username, email, age) VALUES (?, ?, ?)', (f'User{j}', f'user{j}@zmail.ru', 31+j))
for j in range(15):
    cursor.execute('INSERT INTO Users (username, email, age) VALUES (?, ?, ?)', (f'Ruser{j}', f'ruser-{j}@rmail.ru', random.randint(18, 89)))
'''

# Читаем / ищем / выбираем:
# cursor.execute('SELECT * FROM Users') -- выбор всех
cursor.execute('SELECT username, age FROM Users WHERE age >= ?', (39,))  # -- выбор по возрасту
# cursor.execute('SELECT age, email FROM Users GROUP BY age')
users = cursor.fetchall()
for usr in users:
    print(usr)

# Анализ:
# COUNT, SUM, AVG, MIN, MAX, ...
cursor.execute('SELECT AVG(age) FROM Users')
avg_age = cursor.fetchone()[0]
print('avg_age =', avg_age)

cursor.execute('SELECT COUNT(*) FROM Users WHERE age > ?', (avg_age,))
total = cursor.fetchone()[0]
print('total =', total)

cursor.execute('SELECT SUM(age) FROM Users')
s = cursor.fetchone()[0]
print('SUM(age) =', s)

# Обновляем:
'''
cursor.execute('UPDATE Users SET age = ? WHERE username = ?', (77, 'User7'))
'''

# Удаляем:
'''
cursor.execute('DELETE FROM Users WHERE username = ?', ('User8',))
'''

# сохраняем изменения и закрываем соединение с БД:
connection.commit()
connection.close()

