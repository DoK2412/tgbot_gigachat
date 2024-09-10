import asyncio
import logging
import sys
import os
from dotenv import load_dotenv
from servise.state import Form


from aiogram import Bot, Dispatcher, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext




from user.user_verification import User
from servise.base_functions import Menu, Request


load_dotenv()

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user = await User.get_user(message)
    await Menu(message=message).sending_menu(user)


@dp.callback_query(F.data == "Переводчик")
async def gaining_access(callback: types.CallbackQuery, state: FSMContext) -> None:
    user = await User.get_user(callback.message)
    await state.set_state(Form.language)
    await callback.message.answer('Введите на какой язык необходимо перевести текст.')

    # await Request(callback=callback).generation(user)


@dp.message(Form.language)
async def receiving_language(message, state: FSMContext):
    await state.clear()
    user = await User.get_user(message)
    print(message.text)
    user.language = message.text
    await state.set_state(Form.text_translated)
    await message.answer('Введите Ваш текст.')


@dp.message(Form.text_translated)
async def receiving_text(message, state: FSMContext):
    await state.clear()
    user = await User.get_user(message)
    await Request(message=message).translator(user)


async def main() -> None:
    bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())