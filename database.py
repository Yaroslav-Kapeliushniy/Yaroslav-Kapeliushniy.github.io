# database.py
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Initialize the database
engine = create_engine('sqlite:///casino_bot.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# User model
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)  # Telegram user ID
    username = Column(String)
    balance = Column(Float, default=1000.0)  # Starting with 1000 fake money
    games_played = Column(Integer, default=0)
    games_won = Column(Integer, default=0)

# Create tables
Base.metadata.create_all(engine)
