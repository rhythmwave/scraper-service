from scrape.instagram_api.login import get_login_page_and_csrf
import os

# Define filename and path (adjust as needed)
filename = "login_page_data.txt"
filepath = os.path.join(os.getcwd() + '/temp/', filename)  # Get current working directory

# Fetch login page content and CSRF token
login_page_content, csrf_token = get_login_page_and_csrf()

# Check if content retrieved
if login_page_content:
  # Open file in write mode (overwrite existing content)
  with open(filepath, "w", encoding="utf-8") as f:
    # Write login page content
    f.write(login_page_content)
    # If a CSRF token is found, add a newline and write it
    if csrf_token:
      f.write("\nCSRF Token: " + csrf_token)

  print(f"Login page content and (optional) CSRF token saved to: {filepath}")
else:
  print("Failed to retrieve login page content.")
