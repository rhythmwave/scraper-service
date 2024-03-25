from flask import Flask, request, jsonify
from models.users import UserProfile, UserPost, UserReel,UserType  # Import models
from scrape.instagram import scrape_instagram_profile, scrape_instagram_reel, scrape_instagram_photo
import os
from dotenv import load_dotenv
from config import Config
from utils.data import save_data,get_userid_by_username

load_dotenv(verbose=True)
config = Config()

app = Flask(__name__)

# Define a route for scraping Instagram profile data
@app.route('/scrape/instagram', methods=['GET'])
def scrape_profile():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Username parameter is required'}), 400
    
    try:
        profile_data = scrape_instagram_profile(username)
        
        data = {}
        data['type'] = config.TYPE_INSTAGRAM
        data['username'] = profile_data['data']['user']['username']
        data['userid'] = profile_data['data']['user']['id']
        data['full_name'] = profile_data['data']['user']['full_name']
        data['following'] = profile_data['data']['user']['edge_follow']['count']
        data['followers'] = profile_data['data']['user']['edge_followed_by']['count']
        data['bio'] = profile_data['data']['user']['biography']
        data['category'] = profile_data['data']['user']['category_name']
        save_data(data,UserProfile)
        return jsonify({'success': f'Username {data["username"]} is saved'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/scrape/instagram/reel/<username>', methods=['GET'])
def scrape_reel(username):
    if not username:
        return jsonify({'error': 'Username parameter is required'}), 400
    
    # Check if user profile exists
    user_profile = get_userid_by_username(username)  # Replace with your function

    if user_profile is None:
        return jsonify({'error': f'User profile for {username} not found, scrape the user first'}), 404
    try:
        reels = scrape_instagram_reel(user_profile.userid)
        list_media = []
        for item in reels['items']:
            media = item.get('media')
            if media:
                data = {}

                data['userid'] = user_profile.userid
                data['caption'] = media.get('caption', {}).get('text', '')
                data['code'] = media.get('code')
                data['url'] = 'https://www.instagram.com/reel/' + media.get('code')
                data['reel_id'] = media.get('id')
                data['media_type'] = media.get('media_type')
                data['product_type'] = media.get('product_type')
                data['taken_at'] = media.get('taken_at')
                data['video_duration'] = media.get('video_duration')
                data['play_count'] = media.get('play_count')
                data['like_count'] = media.get('like_count')
                data['comment_count'] = media.get('comment_count')
                data['fb_like_count'] = media.get('fb_like_count')
                data['fb_play_count'] = media.get('fb_play_count')
                list_media.append(media.get('code'))
                save_data(data,UserReel)

        return jsonify({'success': f'Reel for username {username} with userid {user_profile.userid} is saved', 'saved_media':list_media}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
