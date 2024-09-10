from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    language = State()            # язык для перевода
    text_translated = State()     # текст для перевода

