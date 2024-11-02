# ставим python 3.9
# ставим aiogram 2.25.2

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import tsukanoff

api = tsukanoff.Telegram.token
bot = Bot(token=api)
dp = Dispatcher(bot=bot, storage=MemoryStorage())

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
button3 = KeyboardButton(text='Купить')
kb.row(button1, button2)
kb.row(button3)

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
    for j in [1, 2, 3, 4]:
        msg = f'Название: Product-{j} | Описание: описание {j} | Цена: {j*100} RUR'
        with open(f'images/photo_{j}.png', 'rb') as img:
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
