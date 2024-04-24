import asyncio
import logging

import googletrans
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from script import TELEGRAM_TOKEN
from googletrans import Translator
from middleware.throttling import AntifloodMiddleware

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.state import StatesGroup, State

storage = MemoryStorage()


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_TOKEN, parse_mode="HTML")

dp = Dispatcher()

# dp.message.middleware(AntifloodMiddleware())
print(googletrans.LANGUAGES)

class UserChoose(StatesGroup):
    choosing_my_lang = State()
    choosing_to_lang = State()


async def main():
    @dp.message(Command("start"))
    async def answer(message: types.Message):
        await message.answer("/Информация/", id='first')


    @dp.message(Command("setmylang"))
    async def setmylang(message: types.Message, state: FSMContext):
        await message.answer(
            text='Выберите Ваш язык'
        )
        await state.set_state(UserChoose.choosing_my_lang)

        # translator = Translator()
        # typ = translator.detect(message.text).lang
        # arr = googletrans.LANGUAGES
        # print(message.text)
        #
        # # if typ == 'ru':
        # #     message = translator.translate(message.text, dest='en', src=typ).text
        # #     main_language = list(filter(lambda key: arr[key] == message, arr))
        # #     print(main_language[0])
        # # elif typ == 'en':
        # #     main_language = list(filter(lambda key: arr[key] == message.text, arr))
        # #     print(main_language[0])
        # # else:
        # #     pass

    @dp.message(UserChoose.choosing_my_lang)
    async def change_my_lang(message: types.Message, state: FSMContext):
        await state.update_data(username=message.text)
        print('123231')
        await state.set_state(UserChoose.choosing_my_lang)


    @dp.message()
    async def talk(message: types.Message):
        main_language = 'ru'
        translator = Translator()

        typ = translator.detect(message.text).lang
        if main_language == typ:
            result = translator.translate(message.text, dest='en', src=typ).text
            first = 'English '
        else:
            result = translator.translate(message.text, dest=main_language, src=typ).text
            first = 'Русский '

        print('message and typetext: ', message.text, typ)
        print('result: ', result)

        await message.answer(f'{first}: {result}')




    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
