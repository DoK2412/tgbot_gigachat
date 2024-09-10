from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from servise.auxiliary_functions import writing_request, authorization_token, translator_text


class Menu(object):

    def __init__(self, message=None, callback=None):
        self.message = message
        self.callback = callback

    async def sending_menu(self, user):
        if user.requests > 0:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Переводчик",
                                         callback_data="Переводчик")
                ],
                [
                    InlineKeyboardButton(text="Генерация изображений",
                                         callback_data="Изображение")
                ],
                [
                    InlineKeyboardButton(text="Генерация текста",
                                         callback_data="Текст")
                ],
                [
                    InlineKeyboardButton(text="Продлить подписку",
                                         callback_data="Подписка")
                ]
            ])
            await self.message.answer('Добро пожаловать в бот генерации на базе GigaChat.', reply_markup=keyboard)
        else:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Добавить запросов",
                                         callback_data="Подписка")
                ]
            ])
            await self.message.answer('У Вас закончились бесплатные запросы.', reply_markup=keyboard)


class Request(object):

    def __init__(self, message=None, callback=None):
        self.message = message
        self.callback = callback

    async def translator(self, user):
        result = await translator_text(user, self.message.text)
        await self.message.answer(f'{result}')
        await self.message.answer(f'Количество запросав уменьшено на 1.\nОсталось: {user.requests}')




