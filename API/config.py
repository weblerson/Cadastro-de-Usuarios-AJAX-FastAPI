from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

CONN = "sqlite:///users.db"

engine = create_engine(CONN, echo = False)

Session = sessionmaker(bind = engine)
session = Session()
Base = declarative_base()