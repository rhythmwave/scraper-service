import os
from dotenv import load_dotenv

class Config:
  def __init__(self):
    load_dotenv()
    self.DATABASE_URL = os.environ.get('DATABASE_URL')
    self.ROCKET_TOKEN = os.environ.get('ROCKETAPI_TOKEN')
    self.INSTA_LIMIT = os.environ.get('INSTA_LIMIT')
    self.TYPE_INSTAGRAM = os.environ.get('TYPE_INSTAGRAM')
