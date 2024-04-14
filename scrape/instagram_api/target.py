import requests
from bs4 import BeautifulSoup
from config.instagram import Config, API, Session
import re
from utils.request import post_process_data,pre_process_request,process_request
import pdb
import urllib.parse

config = Config()
api = API(config)
session = Session()

def target_profile(username):

  endpoint = config.INSTAGRAM_URL + username
  # Replace with a valid user-agent string
  data = {}
  cookie = session.get_cookie()
  headers = {'User-Agent': 'Mozilla/5.0','Cookie':cookie}
  try:
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()  # Raise an exception for non-200 status codes

    soup = BeautifulSoup(response.content, 'html.parser')

    # Target script tag attributes (adjust if needed)
    target_attrs = {'type': 'application/json', 'data-sjs': ''}

    # Regular expression pattern (adjust if needed)
    dtsg_pattern = r'{"dtsg":{?"[^"]+.*?}'
    # dtsg_token_pattern = r'"token":?"([^"]+)"'
    lsd_pattern = r'"LSD":{?"[^"]+.*?}'
    token_pattern = r'"token":?"([^"]+)"'

    # Find the script tag with desired attributes
    target_scripts = soup.find_all('script', attrs=target_attrs)

    for script in target_scripts:
      # Extract script content (assuming JSON is within the text)
      script_content = script.text.strip()

      # Search for the CSRF token using regular expression
      dtsg_match = re.search(dtsg_pattern, script_content)
      lsd_match = re.search(lsd_pattern,script_content)

      if dtsg_match:        
        dtsg = re.search(token_pattern, dtsg_match.group(0))        
        if dtsg:
          data['dtsg_token'] = dtsg.group(1)
      
      if lsd_match:
        lsd = re.search(token_pattern, lsd_match.group(0))        
        if lsd:
          data['lsd_token'] = lsd.group(1)

    # Handle case where no token is found in any script
    if not dtsg_match or not lsd_match:
      print("Token not found in any script tags.")

    return response.text, data

  except requests.exceptions.RequestException as e:
    print(f"Error fetching login page: {e}")
    return None, None
  
def get_profile(data):
  endpoint = api.API_QUERY
  # Replace with a valid user-agent string
  cookie = session.get_cookie()
  headers = {
    'User-Agent': 'Mozilla/5.0',
    'Content-Type':'application/x-www-form-urlencoded',
    'Cookie':cookie
  }

  payload = {
    'av':'17841402286029938',
    '__d':'www',
    '__user':'0',
    '__a':'1',
    '__req':'2',
    '__hs':'19821.HYP:instagram_web_pkg.2.1..0.1',
    'dpr':'1',
    '__ccg':'UNKNOWN',
    '__rev':'1012608719',
    '__s':'zb2muq:hel1p2:c4mq2s',
    '__hsi':'7355443138991490823',
    '__dyn':'7xeUjG1mxu1syUbFp40NonwgU7SbzEdF8aUco2qwJxS0k24o0B-q1ew65xO0FE2awpUO0n24oaEd86a3a1YwBgao6C0Mo2swaOfK0EUjwGzEaE7622362W2K0zK5o4q3y1Sx-0iS2Sq2-azo7u1xwIw8O321LwTwKG1pg2Xwr86C1mwrd6goK68jDyUrAwHyokxK',
    '__csr':'l14ygIxJJiqOh4kBBtHalLqEPb9GGGJy3bGAA9Azbi-tWWFafz9LyF8zlpqybV998SBpq_F28-Jzk8GimbBAJFXhFedyXzeaACyXgjQEniAy8HnyHxR16up2oS-cDyC8xydw05i-wlmmt2E3Jyo1l48wjA1R804GE0q_CoGla1dg4-eCe1cwJwOwjkre13g0OG08ye1Awzg1PEhgkU450378y0AUK7pQaIw02l1w',
    '__comet_req':'7',
    'fb_dtsg':data['dtsg_token'],
    'jazoest':'26279',
    'lsd':data['lsd_token'],
    '__spin_r':'1012608719',
    '__spin_b':'trunk',
    '__spin_t':'1712572560',
    'fb_api_caller_class':'RelayModern',
    'fb_api_req_friendly_name':'PolarisProfilePageContentQuery',
    'variables':'{"id":"40528624","relay_header":false,"render_surface":"PROFILE"}',
    'server_timestamps':'true',
    'doc_id':'7381344031985950'
  }

  try:
    request_data = pre_process_request(
      url=endpoint,
      method="POST",
      headers=headers,
      # cookies=cookie,
      params=urllib.parse.urlencode(payload)
    )

    print(request_data)
  
    response = process_request(request_data)
    
    if response:
      # Process successful response
      response.raise_for_status()

      return response.text, None
    else:
      print("Error: Failed to retrieve data")
  except requests.exceptions.RequestException as e:
    print(f"Error downloading response: {e}")


  return response, None