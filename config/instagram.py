import os
from dotenv import load_dotenv

class Config:
  def __init__(self):
    load_dotenv()
    self.INSTAGRAM_URL = os.environ.get('INSTAGRAM_URL')
    self.INSTAGRAM_USER = os.environ.get('INSTAGRAM_USER')
    self.INSTAGRAM_USERPASS = os.environ.get('INSTAGRAM_USER_PASS')
