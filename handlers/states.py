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

class EditProfile(StatesGroup):
    name = State()
    is_diver = State()
    amount_of_dives = State()
    country = State()
    profile_photo = State()

class Support(StatesGroup):
    message = State()

class AddDive(StatesGroup):
    max_depth = State()
    duration = State()
    water_temperature = State()
    date = State()
    location = State()
    visibility = State()
    dive_type = State()
    dive_center = State()
    dive_buddy = State()
    description = State()
    wetsuit_type = State()
    wetsuit_thickness = State()
    weight = State()
    air_temperature = State()
    air_pressure = State()
    current = State()
    dive_number = State()

