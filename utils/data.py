from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Import your model classes (assuming they are in models.py)
from models import UserProfile, UserPost, UserReel

def save_data(data, model_class, config):
  engine = create_engine(config.DATABASE_URL)
  Session = sessionmaker(bind=engine)
  session = Session(config.DATABASE_URL)
  entry = model_class(**data)  # Create instance using data dictionary
  session.add(entry)
  session.commit()
  session.close()
