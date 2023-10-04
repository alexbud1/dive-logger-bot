from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from caching.cache_language import LanguageCache
from utils import get_phrase
from handlers.states import Support
from aiogram import Bot
import os
from os.path import dirname, join
from dotenv import load_dotenv

router = Router()

# .env adjustments
dotenv_path = join(dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

GROUP_ID=int(os.getenv("GROUP_ID"))

# handle text from user in Support state
@router.message(Support.message, F.text)
async def process_support_message(message: Message, state: FSMContext, bot: Bot) -> None:
    await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "support_message_sent"))  
    message_content = f"📨 <b>Новe повідомлення у підтримку!</b>\n\nID : [{message.from_user.id}]\nІмʼя : {message.from_user.first_name}\nПрізвище : {message.from_user.last_name}\nЮзернейм : {message.from_user.username}\n\nТекст повідомлення : {message.text}"
    print(message.from_user)
    await bot.send_message(GROUP_ID, message_content)

# handle text from user in Support state in group
@router.message(F.text, F.chat.id==GROUP_ID, F.reply_to_message)  
async def process_support_message(message: Message, state: FSMContext, bot: Bot) -> None:
    msg = message.reply_to_message.text if message.reply_to_message.text else message.reply_to_message.caption
    if "ID" in msg:
        id = msg.split("\n")[2].split(" ")[2][1:-1] # find id in message.text
        answer_phrase = get_phrase(await LanguageCache.get_user_language(int(id)), "support_answer")
        message_content = answer_phrase.replace("{answer}", message.text)
        await bot.send_message(int(id), message_content)

# handle photos from user in Support state
@router.message(Support.message, F.photo)
async def process_support_photo(message: Message, state: FSMContext, bot: Bot) -> None:
    await message.answer(get_phrase(await LanguageCache.get_user_language(message.from_user.id), "support_message_sent"))  
    message_content = f"📨 <b>Новe повідомлення у підтримку!</b>\n\nID : [{message.from_user.id}]\nІмʼя : {message.from_user.first_name}\nПрізвище : {message.from_user.last_name}\nЮзернейм : {message.from_user.username}"
    if message.caption:
        message_content += f"\n\nТекст повідомлення : {message.caption}"
    await bot.send_photo(GROUP_ID, message.photo[-1].file_id, caption = message_content)

# handle photos from admin in Support state in group
@router.message(F.photo, F.chat.id==GROUP_ID, F.reply_to_message)
async def process_support_photo(message: Message, state: FSMContext, bot: Bot) -> None:
    msg = message.reply_to_message.text if message.reply_to_message.text else message.reply_to_message.caption
    if "ID" in msg:
        id = msg.split("\n")[2].split(" ")[2][1:-1] # find id in message.text
        if message.caption:
            answer_phrase = get_phrase(await LanguageCache.get_user_language(int(id)), "support_answer")
            message_content = answer_phrase.replace("{answer}", message.caption)
            await bot.send_photo(int(id), message.photo[-1].file_id, caption = message_content)
        else:
            answer_phrase = get_phrase(await LanguageCache.get_user_language(int(id)), "support_answer2")
            await bot.send_photo(int(id), message.photo[-1].file_id, caption = answer_phrase)