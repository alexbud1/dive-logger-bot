from database.config import user_settings
from .cache import MyCache


class LanguageCache(MyCache):

    # Function to get user language preference from cache or database
    @classmethod
    async def get_user_language(cls, user_id: int) -> str:
        # Trying to get the data from the cache
        language = cls.cache.get(user_id)

        if language is not None:
            return language  # Return cached data

        # If not found in the cache, query the database to get the data
        language = await user_settings.get_user_settings(user_id, "language")

        # Store the data in the cache for 4 hours
        cls.cache[user_id] = language
        return language

    # Function to set user language preference
    @classmethod
    async def set_user_language(cls, user_id: int, language_preference: str) -> None:
        # Store the user's language preference in the cache and database
        cls.cache[user_id] = language_preference
        try:
            await user_settings.update_user_settings(
                user_id, "language", language_preference)
        except Exception as e:
            if "User not found" in str(e):
                await user_settings.create_user_settings(
                    user_id, language_preference)
            elif "User settings not modified" in str(e):
                raise Exception("User settings not modified")
            else:
                raise e