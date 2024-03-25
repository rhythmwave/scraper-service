from sqlalchemy import create_engine, Column, Integer, String, JSON, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import Config

Base = declarative_base()
config = Config()
engine = create_engine(config.DATABASE_URL)

class UserType(Base):
    __tablename__ = 'user_types'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    __tableargs__ = {'extend_existing': True}

class UserProfile(Base):
    __tablename__ = 'user_profiles'

    id = Column(Integer, primary_key=True)
    type = Column(Integer)
    username = Column(String,unique=True)
    userid = Column(Integer)
    bio = Column(String)
    category = Column(String)
    full_name = Column(String)
    followers = Column(Integer)
    following = Column(Integer)
    friends = Column(Integer)

    __tableargs__ = {'extend_existing': True}

class UserPost(Base):
    __tablename__ = 'user_posts'

    id = Column(Integer, primary_key=True)
    userid = Column(Integer)
    data = Column(JSON)
    __tableargs__ = {'extend_existing': True}

class UserMedia(Base):
    __tablename__ = 'user_media'

    id = Column(Integer, primary_key=True)
    userid = Column(Integer)
    caption = Column(Text)
    code = Column(String,unique=True)
    url = Column(String)
    reel_id = Column(String)
    media_type = Column(Integer)
    product_type = Column(String)
    taken_at = Column(Integer)
    video_duration = Column(Float)
    play_count = Column(Integer)
    like_count = Column(Integer)
    comment_count = Column(Integer)
    fb_like_count = Column(Integer)
    fb_play_count = Column(Integer)
    __tableargs__ = {'extend_existing': True}


class Comments(Base):
    __tablename__ = 'media_comments'

    id = Column(Integer,primary_key=True)
    comment_id = Column(Integer)
    userid = Column(Integer)
    username = Column(String)
    full_name = Column(String)
    text = Column(Text)
    reel_id = Column(String)
    created_at = Column(Integer)
    index = Column(Integer)
    like_count = Column(Integer)
    child_comment_count = Column(Integer)
    parent_comment_id = Column(Integer)
    replied_to_comment_id = Column(Integer)
    owner_reply_count = Column(Integer)
    __tableargs__ = {'extend_existing': True}

Base.metadata.create_all(engine)
