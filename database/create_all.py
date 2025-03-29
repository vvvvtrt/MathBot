from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base
from database.env import DATABASE_URL

# For create all tables

# Создание движка SQLAlchemy
engine = create_engine(DATABASE_URL)

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

# Создание всех таблиц
Base.metadata.create_all(engine)
