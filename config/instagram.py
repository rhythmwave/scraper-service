import os
from dotenv import load_dotenv
import pdb

class Config:
  def __init__(self):
    load_dotenv()
    self.INSTAGRAM_URL = os.environ.get('INSTAGRAM_URL')
    self.INSTAGRAM_USER = os.environ.get('INSTAGRAM_USER')
    self.INSTAGRAM_USERPASS = os.environ.get('INSTAGRAM_USER_PASS')
    self.HEADER_DATR = os.environ.get('INSTAGRAM_HEADER_DATR')
    self.HEADER_SHBID = os.environ.get('INSTAGRAM_HEADER_SHBID')
    self.HEADER_SHBTS = os.environ.get('INSTAGRAM_HEADER_SHBTS')
    self.HEADER_RUR = os.environ.get('INSTAGRAM_HEADER_RUR')
    self.HEADER_PS_L = os.environ.get('INSTAGRAM_HEADER_PS_L')
    self.HEADER_PS_N = os.environ.get('INSTAGRAM_HEADER_PS_N')    
    self.HEADER_IG_NRCB = os.environ.get('INSTAGRAM_HEADER_IG_NRCB')    

class API:
  def __init__(self,config):
    self.config = config
    self.API_AUTH =  config.INSTAGRAM_URL + 'api/v1/web/accounts/login/ajax/'
    self.API_QUERY = config.INSTAGRAM_URL + 'api/graphql'

class Session:
  
  session_id=''
  cookie={}
  headers={}

  def __init__(self):
    self.id = ''
  
  def set_id(self,session_id):
    self.session_id = session_id
    return True
  
  def set_cookie(self, data):
    
    param = { 
      'csrftoken':data['csrftoken'],
      'ds_user_id':data['ds_user_id'],
      'ig_did':data['ig_did'],
      'mid':data['mid'],
      'ps_l':data['ps_l'],
      'ps_n':data['ps_n'],
      'shbid':data['shbid'],
      'shbts':data['shbts'],
      'rur':data['rur'],
      'csrf_token':data['csrf_token'],
      'sessionid': data['sessionid']
    }

    self.cookie.update(param) 
    return True
  
  def get_cookie(self):
    cookie = 'csrftoken='+self.cookie['csrftoken']+'; ig_did='+self.cookie['ig_did']+'; mid='+self.cookie['mid']+'; ps_l='+self.cookie['ps_l']+'; ps_n='+self.cookie['ps_n']+'; shbid='+self.cookie['shbid']+'; shbts='+self.cookie['shbts']+';rur='+self.cookie['rur']
    
    if 'sessionid' in self.cookie and self.cookie['sessionid']:
      cookie += ';sessionid='+self.cookie['sessionid']
    
    return cookie
  