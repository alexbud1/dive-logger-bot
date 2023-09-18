import asyncio
import os
import ssl
import sys

import certifi
from motor.motor_asyncio import AsyncIOMotorClient

# Add the parent directory to the path so we can import the .env file
sys.path.append("..")
from bot import dotenv_path, load_dotenv

# Import the environment variables from the .env file
load_dotenv(dotenv_path)


class UserSettings:
    def __init__(self, uri: str):
        self._uri = uri  # Store the URI as an instance attribute
        self._client = AsyncIOMotorClient(self._uri, tlsCAFile=certifi.where())

        # Select the database and collection to use
        # Only user_settings is needed for a telegram bot. Other collections are accessed by the API.
        self._db = self._client.dive_logger
        self._user_settings = self._db.user_settings

    # It is used for initializaing the user settings, just after language choice
    async def create_user_settings(self, telegram_id: int, language=None) -> None:
        response = await self._user_settings.insert_one({
            "telegram_id": telegram_id,
            "language": language
        })
        if response.acknowledged == False:
            raise Exception("User settings not created")
        else:
            return response.inserted_id

    # It is used for getting the user settings
    async def get_user_settings(self, telegram_id: int, parameter: str) -> str:
        response = await self._user_settings.find_one({"telegram_id": telegram_id})
        if response:
            if parameter in response:
                return response[parameter]
            else:
                raise Exception("Parameter not found in user settings")
        else:
            await self.create_user_settings(telegram_id)

    # It is used for updating the user settings and if key is not found - it is created
    async def update_user_settings(self, telegram_id: int, parameter: str, value: str) -> None:
        response = await self._user_settings.update_one({"telegram_id": telegram_id}, {"$set": {parameter: value}})
        if response.matched_count == 0:
            raise Exception("User not found")
        elif response.modified_count == 0:
            raise Exception("User settings not modified")

    

    def __repr__(self):
        return f"UserSettings({self.user_id}, {self.language})"


user_settings = UserSettings(os.environ.get("CONNECTION_URI"))

# async def main():
#     user_settings = UserSettings(os.environ.get("CONNECTION_URI"))
#     found = await user_settings.create_user_settings(232342343290, "lang_eng")
#     print(found)

# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
