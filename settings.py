import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent

CREDENTIALS_FILE = BASE_DIR / 'security/creds.json'
FILE_ID = '1uByXNyyganJjvru5Ggv9HYXq1qhFYc3GNFiuxHSeAVU'
SCHEDULE_NAME = 'schedule.xlsx'

TOKEN = os.getenv('TOKEN')

DATABASE = {
    'ENGINE': os.getenv('DB_ENGINE'),
    'NAME': os.getenv('DB_NAME'),
    'USER': os.getenv('DB_USER'),
    'PASSWORD': os.getenv('DB_PASSWORD'),
}

# DATABASE = {
#     'ENGINE': 'sqlite3',
#     'NAME': 'db.sqlite',
# }
