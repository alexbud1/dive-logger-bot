from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from caching.cache_language import LanguageCache
from handlers.states import FillProfile
from utils import get_phrase
from keyboards.keyboards import (
    is_diver_keyboard
)
router = Router()

# handle name entered by user for his profile
@router.message(FillProfile.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(FillProfile.is_diver)

    phrase = get_phrase(await LanguageCache.get_user_language(message.from_user.id), "is_diver").replace("{name}", message.text)
    await message.answer(phrase, reply_markup=is_diver_keyboard.as_markup())