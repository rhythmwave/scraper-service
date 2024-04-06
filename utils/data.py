from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models.users import UserProfile, Comments, UserMedia
from config.main import Config

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
    elif model_class.__name__ == "UserMedia":
        # Check if code exists
        existing_entry = session.query(UserMedia).filter(UserMedia.code == data['code']).first()
    elif model_class.__name__ == "Comments":
        # Check if code exists
        existing_entry = session.query(Comments).filter(Comments.comment_id == data['comment_id']).first()

    if existing_entry:
        for key, value in data.items():
            setattr(existing_entry, key, value)
        
        session.commit()
    else:
        # Save the data
        session.add(model_class(**data))
        session.commit()
        print("Data saved successfully.")
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

def get_mediaid_by_usernid_n_code(userid,code):
  try:
    res = session.query(UserMedia).filter(UserMedia.userid == userid,UserMedia.code == code).first()
    return res
  except Exception as e:
    # Handle potential database errors
    print(f"Error querying user profile for {userid}: {e}")
    return None