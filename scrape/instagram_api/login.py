import requests
from bs4 import BeautifulSoup
from config.instagram import Config
import re

config = Config()

def get_login_page_and_csrf(url=config.INSTAGRAM_URL):

  # Replace with a valid user-agent string
  headers = {'User-Agent': 'Mozilla/5.0'}
  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for non-200 status codes

    soup = BeautifulSoup(response.content, 'html.parser')

    # Target script tag attributes (adjust if needed)
    target_attrs = {'type': 'application/json', 'data-sjs': ''}

    # Regular expression pattern (adjust if needed)
    pattern = r'"csrf_token": ?"([^"]+)"'

    # Find the script tag with desired attributes
    target_scripts = soup.find_all('script', attrs=target_attrs)

    csrf_token = ''

    for script in target_scripts:
      # Extract script content (assuming JSON is within the text)
      script_content = script.text.strip()

      # Search for the CSRF token using regular expression
      match = re.search(pattern, script_content)

      if match:
        # Extract the captured group (CSRF token value)
        csrf_token = match.group(1)
        print("CSRF token found:", csrf_token)
        break  # Exit the loop after finding the token

    # Handle case where no token is found in any script
    if not match:
      print("CSRF token not found in any script tags.")

    return response.text, csrf_token

  except requests.exceptions.RequestException as e:
    print(f"Error fetching login page: {e}")
    return None, None

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
