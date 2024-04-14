from scrape.instagram_api.login import get_login_page_and_csrf, auth as instagram_auth
from scrape.instagram_api.target import target_profile,get_profile
import os
from config.instagram import Config
from utils.request import save_http_response
import pdb

config = Config()

# Define filename and path (adjust as needed)
filename = "login_page_data.txt"
fileauth = "auth_response.txt"
filepath = os.path.join(os.getcwd() + '/temp/', filename)  # Get current working directory
fileauthpath = os.path.join(os.getcwd() + '/temp/', fileauth)  # Get current working directory

# Fetch login page content and CSRF token
login_page_content, data = get_login_page_and_csrf()

response_auth, data = instagram_auth(config.INSTAGRAM_USER, config.INSTAGRAM_USERPASS, data)

# Check if content retrieved
if login_page_content:
  # Open file in write mode (overwrite existing content)
  with open(filepath, "w", encoding="utf-8") as f:
    # Write login page content
    f.write(login_page_content)
    # If a CSRF token is found, add a newline and write it
    # if data:
    #   f.write(data)

  print(f"Login page content and (optional) CSRF token saved to: {filepath}")
else:
  print("Failed to retrieve login page content.")

# Fetch target page content and token
target_page, target_data = target_profile('ridwankamil')
# Check if content retrieved
if target_page:
  # Open file in write mode (overwrite existing content)
  targetpath = os.path.join(os.getcwd() + '/temp/target_page.txt')
  with open(targetpath, "w", encoding="utf-8") as f:
    # Write login page content
    f.write(target_page)
    # If a CSRF token is found, add a newline and write it
    # if data:
    #   f.write(data)

  print(f"Target page content and (optional) token saved to: {targetpath}")
else:
  print("Failed to retrieve target page content.")

# Fetch target profile
target_profile, target_profile_data = get_profile(target_data)

# Check if content retrieved
if target_profile:
  # Open file in write mode (overwrite existing content)
  target_profilepath = os.path.join(os.getcwd() + '/temp/target_profile.txt')
  with open(target_profilepath, "w", encoding="utf-8") as f:
    # Write login page content
    f.write(target_profile)
    # If a CSRF token is found, add a newline and write it
    # if data:
    #   f.write(data)

  print(f"Target page content and (optional) token saved to: {target_profilepath}")
else:
  print("Failed to retrieve target page content.")

if response_auth:
    with open(fileauthpath, "w", encoding="utf-8") as f:
      save_http_response(response_auth,fileauthpath)