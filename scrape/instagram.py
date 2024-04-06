from rocketapi import InstagramAPI
from scrape.instagram_api.login import get_login_page_and_csrf
from config.main import Config

config = Config()
rocket = InstagramAPI(token=config.ROCKET_TOKEN)

def scrape_instagram_profile(username):
    try:
        if config.TYPE_INSTAGRAM == 1:
            profile_data = rocket.get_user_info(username=username)
        elif config.TYPE_INSTAGRAM == 2:
            login, token = get_login_page_and_csrf()
            print(login)
            print(token)
        return profile_data
    except Exception as e:
        raise Exception("Error scraping profile data: " + str(e))

def scrape_instagram_media(userid,count = config.INSTA_LIMIT):
    try:
        posts_data = rocket.get_user_media(userid,count)
        return posts_data
    except Exception as e:
        raise Exception("Error scraping reel data: " + str(e))
    
def scrape_instagram_comment(mediaid,count = config.INSTA_LIMIT):
    try:
        posts_data = rocket.get_media_comments(mediaid)
        return posts_data
    except Exception as e:
        raise Exception("Error scraping comments data: " + str(e))