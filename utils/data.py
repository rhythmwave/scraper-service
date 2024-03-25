from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models.users import UserProfile, UserPost, UserReel
from config import Config

config = Config()

# Create a scoped session factory outside of functions
engine = create_engine(config.DATABASE_URL)  # Create the engine once
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a global session outside of functions
session = SessionLocal()  # Global session

def save_data(data, model_class):
  try:
    if model_class.__name__ == "UserProfile":
        # Check if username or userid exists
        existing_entry = session.query(UserProfile).filter(UserProfile.username == data['username'] or UserProfile.userid == data['userid']).first()
        if existing_entry:            
            for key, value in data.items():
                setattr(existing_entry, key, value)
            
            session.commit()
        else:
            # Save the data
            session.add(model_class(**data))
            session.commit()
            print("Data saved successfully.")
    elif model_class.__name__ == "UserReel":
        # Check if code exists
        existing_entry = session.query(UserReel).filter(UserReel.code == data['code']).first()
        if existing_entry:
            for key, value in data.items():
                setattr(existing_entry, key, value)
            
            session.commit()
        else:
            # Save the data
            session.add(model_class(**data))
            session.commit()
            print("Data saved successfully.")
    else:
        print("Invalid model.")
  except Exception as e:
    session.rollback()  # Rollback on errors
    raise e

def get_userid_by_username(username):
  try:
    user_profile = session.query(UserProfile).filter_by(username=username).first()
    return user_profile
  except Exception as e:
    # Handle potential database errors
    print(f"Error querying user profile for {username}: {e}")
    return None

