from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
import json

language_keyboard = InlineKeyboardBuilder()
language_keyboard.add(InlineKeyboardButton(text="English 🇺🇸", callback_data='lang_en'),
    InlineKeyboardButton(text="Українська 🇺🇦", callback_data='lang_ukr')
)