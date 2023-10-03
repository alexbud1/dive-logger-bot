from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class FillProfile(StatesGroup):
    name = State()
    is_diver = State()
    amount_of_dives = State()
    country = State()
    profile_photo = State()

class Settings(StatesGroup):
    language = State()
    # profile_photo = State()

class EditProfile(StatesGroup):
    name = State()
    is_diver = State()
    amount_of_dives = State()
    country = State()
    profile_photo = State()

class Support(StatesGroup):
    message = State()