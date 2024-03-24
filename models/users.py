from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import Config

Base = declarative_base()
config = Config()
engine = create_engine(config.DATABASE_URL)

class UserProfile(Base):
    __tablename__ = 'user_profiles'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    data = Column(JSON)

class UserPost(Base):
    __tablename__ = 'user_posts'

    id = Column(Integer, primary_key=True)
    userid = Column(Integer)
    data = Column(JSON)

class UserReel(Base):
    __tablename__ = 'user_reels'

    id = Column(Integer, primary_key=True)
    userid = Column(Integer)
    data = Column(JSON)

Base.metadata.create_all(engine)
