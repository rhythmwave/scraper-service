from rocketapi import InstagramAPI

rocket = InstagramAPI(token="Dpcs2WCnfvpRpYa5C_F3kA")

def scrape_profile(username):
    try:
        profile_data = rocket.get_user_info(username=username)
        return profile_data
    except Exception as e:
        raise Exception("Error scraping profile data: " + str(e))

def scrape_reel(userid,count = 20):
    try:
        posts_data = rocket.get_user_clips(userid,count)
        return posts_data
    except Exception as e:
        raise Exception("Error scraping reel data: " + str(e))
    
def scrape_photo(userid,count = 20):
    try:
        posts_data = rocket.get_user_clips(userid,count)
        return posts_data
    except Exception as e:
        raise Exception("Error scraping photo data: " + str(e))