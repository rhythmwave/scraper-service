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

def get_login_page_and_csrf(url=config.INSTAGRAM_URL):

  # Replace with a valid user-agent string
  data = {}
  headers = {'User-Agent': 'Mozilla/5.0'}
  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for non-200 status codes

    soup = BeautifulSoup(response.content, 'html.parser')

    # Target script tag attributes (adjust if needed)
    target_attrs = {'type': 'application/json', 'data-sjs': ''}

    # Regular expression pattern (adjust if needed)
    polaris_data_pattern = r'\["PolarisSiteData".*?\].*?\]'
    csrf_pattern = r'"csrf_token": ?"([^"]+)"'
    device_id_pattern = r'"device_id": ?"([^"]+)"'
    machine_id_pattern = r'"machine_id": ?"([^"]+).*?"'
    app_id_pattern = r'"X-IG-App-ID": ?"([^"]+).*?"'

    # Find the script tag with desired attributes
    target_scripts = soup.find_all('script', attrs=target_attrs)

    csrf_token = ''

    for script in target_scripts:
      # Extract script content (assuming JSON is within the text)
      script_content = script.text.strip()

      # Search for the CSRF token using regular expression
      match = re.search(csrf_pattern, script_content)
      data_match = re.search(polaris_data_pattern,script_content)

      if match:
        # Extract the captured group (CSRF token value)
        csrf_token = match.group(1)
        if data_match:
          machindeid_match = re.search(machine_id_pattern, data_match.group(0))
          deviceid_match = re.search(device_id_pattern, data_match.group(0))
          ig_app_id_match = re.search(app_id_pattern, script_content)
          data['machine_id'] = machindeid_match.group(1)          
          data['device_id'] = deviceid_match.group(1)
          data['app_id'] = ig_app_id_match.group(1)
        data['csrf_token'] = csrf_token
        print("CSRF token found:", csrf_token)

        break  # Exit the loop after finding the token

    # Handle case where no token is found in any script
    if not match:
      print("CSRF token not found in any script tags.")

    return response.text, data

  except requests.exceptions.RequestException as e:
    print(f"Error fetching login page: {e}")
    return None, None

def auth(username=None,password=None,data={}):
  
  endpoint = api.API_AUTH
  session_data = {}
  cookie = 'csrftoken='+data['csrf_token']+'; ig_did='+data['device_id']+'; mid='+data['machine_id']+'; ps_l='+config.HEADER_PS_L+'; ps_n='+config.HEADER_PS_N+'; shbid='+config.HEADER_SHBID+'; shbts='+config.HEADER_SHBTS
  headers = {
    'X-CSRFToken': data['csrf_token'],
    'X-IG-App-ID': data['app_id'],
    'X-Instagram-AJAX': '1012608719',
    'X-ASBD-ID': '129477',
    'X-IG-WWW-Claim': '0',
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://www.instagram.com',
    'Alt-User': 'www.instagram.com',
    'Cookie': cookie
  }

  payload = {
    'enc_password': config.INSTAGRAM_USERPASS,
    'optIntoOneTap': False,
    'trustedDeviceRecords': '{}',
    'queryParams': '{}',
    'username': config.INSTAGRAM_USER
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
      session.set_id(response.cookies['sessionid'])
      # processed_data = post_process_data(response.json(), headers=response.headers)
      session_data['csrftoken'] = response.cookies['csrftoken']
      session_data['ds_user_id'] = response.cookies['ds_user_id']
      session_data['ig_did'] = data['device_id']
      session_data['mid'] = data['machine_id']
      session_data['ps_l'] = config.HEADER_PS_L
      session_data['ps_n'] = config.HEADER_PS_N
      session_data['shbid'] = '"'+config.HEADER_SHBID+'"'
      session_data['shbts'] = '"'+config.HEADER_SHBTS+'"'
      session_data['rur'] = response.cookies['rur']
      session_data['csrf_token'] = data['csrf_token']
      session_data['sessionid'] = response.cookies['sessionid']
      session.set_cookie(session_data)
      # print(processed_data)

      return response, None
    else:
      print("Error: Failed to retrieve data")
  except requests.exceptions.RequestException as e:
    print(f"Error downloading response: {e}")


  return response, None


    
# Example usage
# login_url = "https://www.instagram.com/accounts/login/"  # Replace if needed
# login_page_content, csrf_token = get_login_page_and_csrf(login_url)

# if login_page_content:
#   if csrf_token:
#     print(f"Login page content retrieved. CSRF token: {csrf_token}")
#   else:
#     print("Login page content retrieved, but CSRF token not found in the HTML.")
# else:
#   print("Failed to retrieve login page content.")
