import requests
from bs4 import BeautifulSoup

def scrape_instagram_profile(username):
  """
  Scrapes basic information from a public Instagram profile using web scraping.

  Args:
      username: The username of the Instagram profile to scrape.

  Returns:
      A dictionary containing scraped information (if successful), or None if unsuccessful.
  """

  # Replace with a valid user-agent string
  headers = {'User-Agent': 'Mozilla/5.0'}
  url = f"https://www.instagram.com/{username}/"

  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for non-200 status codes

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract profile information (replace/adjust selectors as needed)
    profile_pic = soup.find('img', {'alt': 'Profile picture'})['src']  # Assuming profile picture

    # ... (extract other desired information using appropriate selectors)

    return {
      'username': username,
      'profile_pic': profile_pic,
      # ... (add other scraped data)
    }

  except requests.exceptions.RequestException as e:
    print(f"Error scraping profile for {username}: {e}")
    return None
