import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()


ICON_PATH = "./media/icon.png"
DEFAULT_PHOTO_PATH = "./media/default_good.png"

DEFAULT_WINDOW_TITLE = "OOO «Обувь»"

DB_CONNECTOR = "mysql+mysqlconnector"
DB_USER = "test_user"
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "exam_sample1"

DB_ENGINE = create_engine(f"{DB_CONNECTOR}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
