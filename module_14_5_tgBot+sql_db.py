# ставим python 3.9
# ставим aiogram 2.25.2

'''Задача "Регистрация покупателей":
Подготовка:
Для решения этой задачи вам понадобится код из предыдущей задачи.
Дополните его, следуя пунктам задачи ниже.

Дополните файл crud_functions.py, написав и дополнив в нём следующие функции:
initiate_db дополните созданием таблицы Users, если она ещё не создана при помощи SQL запроса.
Эта таблица должна содержать следующие поля:
id - целое число, первичный ключ
username - текст (не пустой)
email - текст (не пустой)
age - целое число (не пустой)
balance - целое число (не пустой)

add_user(username, email, age), которая принимает: имя пользователя, почту и возраст.
Данная функция должна добавлять в таблицу Users вашей БД запись с переданными данными.
Баланс у новых пользователей всегда равен 1000. Для добавления записей в таблице используйте SQL запрос.

is_included(username) принимает имя пользователя и возвращает True, если такой пользователь есть в таблице Users,
в противном случае False. Для получения записей используйте SQL запрос.

Изменения в Telegram-бот:
Кнопки главного меню дополните кнопкой "Регистрация".
Напишите новый класс состояний RegistrationState с следующими объектами класса State:
username, email, age, balance(по умолчанию 1000).
'''
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
import asyncio
import crud_functions as crud
import tsukanoff

logging.basicConfig(level=logging.INFO)

token = tsukanoff.Telegram.token
bot = Bot(token=token)
dp = Dispatcher(bot=bot, storage=MemoryStorage())

# считываем из db в global var.:
products = crud.get_all_products()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

ikb = InlineKeyboardMarkup()
button1i = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2i = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
ikb.add(button1i)
ikb.add(button2i)

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Регистрация')
button4 = KeyboardButton(text='Купить')
kb.row(button1, button2)
kb.row(button3, button4)

buy_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton('Product-1', callback_data='product_buying')],
        [InlineKeyboardButton('Product-2', callback_data='product_buying')],
        [InlineKeyboardButton('Product-3', callback_data='product_buying')],
        [InlineKeyboardButton('Product-4', callback_data='product_buying')]
    ], resize_keyboard=True
)

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=ikb)

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer(f'Здравствуйте, {message.from_user.username}!\n'
                         'Я -- бот, помогающий Вашему здоровью.',
                         reply_markup=kb)

'''
Создайте цепочку изменений состояний RegistrationState.
Функции цепочки состояний RegistrationState:

sing_up(message):
Оберните её в message_handler, который реагирует на текстовое сообщение 'Регистрация'.
Эта функция должна выводить в Telegram-бот сообщение "Введите имя пользователя (только латинский алфавит):".
После ожидать ввода имени в атрибут RegistrationState.username при помощи метода set.
'''
@dp.message_handler(text=['Регистрация'])
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()
'''
set_username(message, state):
Оберните её в message_handler, который реагирует на состояние RegistrationState.username.
Если пользователя message.text ещё нет в таблице, то должны обновляться данные в состоянии username на message.text.
Далее выводится сообщение "Введите свой email:" и принимается новое состояние RegistrationState.email.
Если пользователь с таким message.text есть в таблице, то выводить "Пользователь существует, введите другое имя" и
запрашивать новое состояние для RegistrationState.username.
'''
@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if not crud.is_included(message.text):
        await state.update_data(username=message.text)
        await message.answer('Введите свой e-mail:')
        await RegistrationState.email.set()
    else:
        await message.answer('Пользователь с таким именем уже существует, пожалуйста, введите другое имя:')
        await RegistrationState.username.set()
'''
set_email(message, state):
Оберните её в message_handler, который реагирует на состояние RegistrationState.email.
Эта функция должна обновляться данные в состоянии RegistrationState.email на message.text.
Далее выводить сообщение "Введите свой возраст:":
После ожидать ввода возраста в атрибут RegistrationState.age.
'''
@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    # проверим на наличие собаки @ и точки:
    if ('@' in message.text) and ('.' in message.text):
        await state.update_data(email=message.text)
        await message.answer('Введите свой возраст:')
        await RegistrationState.age.set()
    else:
        await message.answer('Неверный формат эл.почты, введите, пожалуйста, другой адрес:')
        await RegistrationState.email.set()

'''
set_age(message, state):
Оберните её в message_handler, который реагирует на состояние RegistrationState.age.
Эта функция должна обновлять данные в состоянии RegistrationState.age на message.text.
Далее брать все данные (username, email и age) из состояния и записывать в таблицу Users при помощи ранее написанной crud-функции add_user.
'''
@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    try:
        age = int(message.text)
    except:
        await message.answer(f'Не могу конвертировать возраст в целое число. Введите ещё раз:')
        await RegistrationState.age.set()
        return
    await state.update_data(age=message.text)
    data = await state.get_data()
    # если все ок, добавляем в db:
    crud.add_user(data['username'], data['email'], int(data['age']))
    await message.answer('Спасибо за регистрацию!')
    await state.finish()
'''
В конце завершать приём состояний при помощи метода finish().
Перед запуском бота пополните вашу таблицу Products 4 или более записями для последующего вывода в чате Telegram-бота.'''

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()  # для деактивации кнопки после нажатия

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    msg = 'Упрощенный вариант формулы Миффлина-Сан Жеора:\n'\
          'для мужчин: 10 х вес (кг) + 6.25 x рост (см) – 5 х возраст (г) + 5\n'\
          'для женщин: 10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) – 161'
    await call.message.answer(msg)
    await call.answer()

@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Я -- бот, рассчитывающий норму ккал по упрощенной формуле Миффлина-Сан Жеора.')

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост (см):')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес (кг):')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()

    try:
        age = float(data['age'])
        weight = float(data['weight'])
        growth = float(data['growth'])
    except:
        await message.answer(f'Не могу конвертировать введенные значения в числа.')
        await state.finish()
        return

    # Упрощенный вариант формулы Миффлина-Сан Жеора:
    # для мужчин: 10 х вес (кг) + 6.25 x рост (см) – 5 х возраст (г) + 5
    calories_man = 10 * weight + 6.25 * growth - 5 * age + 5
    # для женщин: 10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) – 161
    calories_wom = 10 * weight + 6.25 * growth - 5 * age - 161
    await message.answer(f'Норма (муж.): {calories_man} ккал или {round(calories_man*4.184)} кДж')
    await message.answer(f'Норма (жен.): {calories_wom} ккал или {round(calories_wom*4.184)} кДж')
    await state.finish()

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    global products
    for p in products:
        msg = f'Название: {p[1]} | Описание: {p[2]} | Цена: {p[3]} RUR'
        with open(f'images/{p[4]}.png', 'rb') as img:
            await message.answer_photo(img, msg)
    await message.answer('Выберите продукт для покупки:', reply_markup=buy_kb)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

@dp.message_handler()
async def all_messages(message):
    await message.answer('Для начала, пожалуйста, нажмите на команду /start')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
