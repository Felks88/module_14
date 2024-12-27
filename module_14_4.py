from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from crud_functions import *

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


kb = ReplyKeyboardMarkup(resize_keyboard=True)
but = KeyboardButton('Информация')
but2 = KeyboardButton('Рассчитать')
but3 = KeyboardButton('Купить')

kb.row(but, but2)
kb.add(but3)

kb2 = InlineKeyboardMarkup()
but = InlineKeyboardButton('Product1', callback_data='product_buying')
but2 = InlineKeyboardButton('Product2', callback_data='product_buying')
but3 = InlineKeyboardButton('Product3', callback_data='product_buying')
but4 = InlineKeyboardButton('Product4', callback_data='product_buying')
kb2.row(but, but2, but3, but4)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    products = get_all_products()
    picture = 1
    for i in products:
        await message.answer(f'Название: {i[1]} | Описание: {i[2]} | Цена: {i[3]}')
        with open(f'C:/Users/Deep Cool/Downloads/{picture}.WEBP', "rb") as img:
            await message.answer_photo(img, f'Продукт {picture}')
        picture += 1
    await message.answer('Выберите продукт для покупки:', reply_markup=kb2)
    # with open('C:/Users/Deep Cool/Downloads/Pivo.WEBP', 'rb') as img:
    #     await message.answer_photo(img, 'Название: Product1 | Для прибавки веса | Цена: 100')
    # with open('C:/Users/Deep Cool/Downloads/Stolichnaia.WEBP', 'rb') as img:
    #     await message.answer_photo(img, 'Название: Product2 | Быстрые калории | Цена: 200')
    # with open('C:/Users/Deep Cool/Downloads/Whisky.WEBP', 'rb') as img:
    #     await message.answer_photo(img, 'Название: Product3 | Для настроения | Цена: 300')
    # with open('C:/Users/Deep Cool/Downloads/Spirt.WEBP', 'rb') as img:
    #     await message.answer_photo(img, 'Название: Product4 | Для разочарований | Цена: 400')
    #     await message.answer('Выберите продукт для покупки::', reply_markup=kb2)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью. Давай рассчитаем суточную норму калорий.',
                         reply_markup=kb)


@dp.message_handler(text='Информация')
async def hello_message(message):
    await message.answer('Также Вашему вниманию представлен перечень наших товаров.'
                         'Для просмотра нажмите кнопке "Купить"')


@dp.message_handler(text='Рассчитать')
async def hello_message(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    await message.answer(f'Ваши калории в сутки:'
                         f'{int((10 * int(data["weight"]) + 6.25 * int(data["growth"]) - 5 * int(data["age"]) + 5))}')
    await state.finish()


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
