from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Import your model classes (assuming they are in models.py)
from models.users import UserProfile, UserPost, UserReel

def save_data(data, model_class, config):
  # Create the engine outside the function (assuming it's constant)
  engine = create_engine(config.DATABASE_URL)  # Create the engine once

  # Create a session maker using only the engine
  SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

  # Use the session maker to create a session
  with SessionLocal() as session:
    # Check if username or userid exists
    existing_entry = session.query(model_class).filter_by(
        username=data['username'],  # Check by username
        # OR
        # userid=data['userid']  # Check by userid (if available)
    ).first()

    if existing_entry:
      # Update existing entry
      for key, value in data.items():
        setattr(existing_entry, key, value)
    else:
      # Create new entry if not found
      entry = model_class(**data)
      session.add(entry)

    session.commit()

def get_userid_by_username(username, session):
  """
  Queries the database for a user profile based on the provided username.

  Args:
      username: The username to search for.
      session: A database session object (obtained from your application).

  Returns:
      A UserProfile object if found, otherwise None.
  """

  try:
    user_profile = session.query(UserProfile).filter_by(username=username).first()
    return user_profile
  except Exception as e:
    # Handle potential database errors
    print(f"Error querying user profile for {username}: {e}")
    return None

