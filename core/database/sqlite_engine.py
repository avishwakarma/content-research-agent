from sqlalchemy import create_engine
from config import Config

engine = create_engine(Config.database_url, echo=True)
