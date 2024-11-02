import sqlite3
'''Цель: научится использовать функции внутри запросов языка SQL и использовать их в решении задачи.

Задача "Средний баланс пользователя":
Для решения этой задачи вам понадобится решение предыдущей.
Для решения необходимо дополнить существующий код:
Удалите из базы данных not_telegram.db запись с id = 6.
Подсчитать общее количество записей.
Посчитать сумму всех балансов.
Вывести в консоль средний баланс всех пользователей.
'''
connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

#посмотрим, что есть:
print('Было:')
cursor.execute('SELECT * FROM Users')
for u in cursor.fetchall():
    print(u)
# удаляем 6-ой:
cursor.execute('DELETE FROM Users WHERE id = ?', (6,))
print('Стало:')
cursor.execute('SELECT * FROM Users')
for u in cursor.fetchall():
    print(u)

# Подсчет количества:
cursor.execute('SELECT COUNT(*) FROM Users')
count = cursor.fetchone()[0]
cursor.execute('SELECT SUM(balance) FROM Users')
total = cursor.fetchone()[0]
print(f'COUNT(*) = {count}')
print(f'SUM(balance) = {total}')
print(f'Средний баланс: {total/count}')

# сохраняем изменения и закрываем соединение с БД:
connection.commit()
connection.close()
'''
Пример результата выполнения программы:
Выполняемый код:
# Код из предыдущего задания
# Удаление пользователя с id=6
# Подсчёт кол-ва всех пользователей
# Подсчёт суммы всех балансов
print(all_balances / total_users)
connection.close()

Вывод на консоль:
700.0

Файл module_14_2.py с кодом и базу данных not_telegram.db загрузите на ваш GitHub репозиторий. В решении пришлите ссылку на него.'''