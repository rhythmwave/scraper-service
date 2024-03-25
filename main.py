from flask import Flask, request, jsonify
from models.users import UserProfile, UserPost, UserReel,UserType  # Import models
from scrape.instagram import scrape_instagram_profile, scrape_instagram_reel, scrape_instagram_photo
import os
from dotenv import load_dotenv
from config import Config
from utils.data import save_data

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
        save_data(data,UserProfile,config)
        return jsonify({'success': f'Username {data["username"]} is saved'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
