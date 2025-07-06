import os
from dotenv import load_dotenv

__all__ = ["cfg", "__cfg__"]
load_dotenv()
ENVIRONMENT = os.getenv("ENVIRONMENT")
DATABASE_URL = os.getenv("DATABASE_URL")
ALGORITHM = os.getenv("ALGORITHM")
APP_NAME = os.getenv("APP_NAME")
JWT_SECRET = os.getenv("JWT_SECRET")
USDA_API_KEY = os.getenv("USDA_API_KEY")
# required environment variables

__cfg__ = {
    "ENVIRONMENT": ENVIRONMENT,
    "APP_NAME": APP_NAME,
    "JWT_SECRET": JWT_SECRET,
    "DATABASE_URL": DATABASE_URL,
    "ALGORITHM": ALGORITHM,
    "USDA_API_KEY": USDA_API_KEY,
}

def is_prod():
    return ENVIRONMENT == "prod"


def is_dev():
    return ENVIRONMENT == "dev"


def is_qa():
    return ENVIRONMENT == "qa"


def is_staging():
    return ENVIRONMENT == "staging"

# query
def cfg(key: str):
    return __cfg__.get(key) or os.getenv(key)
