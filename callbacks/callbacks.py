from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.types import Message
from caching.cache_language import LanguageCache
from utils import get_phrase
router = Router()

@router.callback_query(F.data.startswith('lang_'))
async def send_random_value(callback: types.CallbackQuery):
    try:
        await LanguageCache.set_user_language(callback.from_user.id, callback.data)
    except Exception as e:
        if "User settings not modified" in str(e):
            await callback.message.edit_text(get_phrase("lang_en", "language_changed"))
        else:
            raise e

    language = await LanguageCache.get_user_language(callback.from_user.id)
    await callback.message.edit_text(get_phrase(language, "language_changed"))
    await callback.answer()