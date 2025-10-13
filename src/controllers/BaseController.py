from dotenv import load_dotenv
import os

from helpers import Settings

load_dotenv()


class BaseController:
    def __init__(self):
        self.settings = Settings()

        self.ASSETS_PATH = self.settings.ASSETS_FOLDER
        if not os.path.exists(self.ASSETS_PATH):
            os.mkdir(self.ASSETS_PATH)

        self.RAW_DATA_PATH = os.path.join(self.ASSETS_PATH, "RawData")
        