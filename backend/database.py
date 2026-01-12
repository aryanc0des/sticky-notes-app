from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQL_ALCHEMY_DATABASE_URL = 'sqlite:///./notes.db'

db_engine = create_engine(SQL_ALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

LocalSession = sessionmaker(bind=db_engine, autocommit=False, autoflush=False)

Base = declarative_base()