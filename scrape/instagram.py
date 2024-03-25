from rocketapi import InstagramAPI
from config import Config
import json

config = Config()
rocket = InstagramAPI(token=config.ROCKET_TOKEN)

def scrape_instagram_profile(username):
    try:
        profile_data = rocket.get_user_info(username=username)
        return profile_data
    except Exception as e:
        raise Exception("Error scraping profile data: " + str(e))

def scrape_instagram_reel(userid,count = config.INSTA_LIMIT):
    try:
        posts_data = rocket.get_user_clips(userid,count)
        return posts_data
    except Exception as e:
        raise Exception("Error scraping reel data: " + str(e))
    
def scrape_instagram_photo(userid,count = config.INSTA_LIMIT):
    try:
        posts_data = rocket.get_user_clips(userid,count)
        return posts_data
    except Exception as e:
        raise Exception("Error scraping photo data: " + str(e))