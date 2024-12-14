"""
coding: utf-8
Дегтярев Виталий (группа 22/08)
Домашнее задание №13.5
Домашнее задание по теме "Клавиатура кнопок"
"""


from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio


# Инициализация Телеграм-бота
api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage= MemoryStorage())


# Определение класса состояний
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


# Инициализация визуальной клавиатуры
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.add(button)
kb.insert(button2)


# Стартовая функция
@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью", reply_markup = kb)


# Блок функций машины состояний для расчета калорий
@dp.message_handler(text="Рассчитать")
async def set_age(message):
    await message.answer("Введите свой возраст")
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    data['calories'] = 10*int(data['weight'])+6.25*int(data['growth'])-5*int(data['age'])+5
    await message.answer(f"Ваша норма калорий (для мужчины) составляет: {data['calories']} кал")
    await state.finish()


# Блок информации
@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('https://www.calc.ru/Formula-Mifflinasan-Zheora.html')


# Реакция на прочие сообщения пользователя
@dp.message_handler()
async def all_message(message):
    await message.answer("Введите команду /start, чтобы начать общение.")


# Запуск Телеграм-бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)