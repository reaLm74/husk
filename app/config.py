import os

from dotenv import load_dotenv

load_dotenv()

base_dir = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
    base_dir, '..', 'app.db'
)
DATABASE = 'app.db'

SECRET_KEY = os.getenv('SECRET_KEY')
