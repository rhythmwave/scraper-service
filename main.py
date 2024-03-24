from flask import Flask, request, jsonify
from models.users import UserProfile, UserPost, UserReel  # Import models
from scrape.instagram import scrape_profile_data, scrape_posts_data, scrape_reels_data
import os
from dotenv import load_dotenv
from config import Config
from utils.data import save_data

load_dotenv(verbose=True)
config = Config()

app = Flask(__name__)

# Define a route for scraping Instagram profile data
@app.route('/scrape/profile', methods=['GET'])
def scrape_profile():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Username parameter is required'}), 400
    
    try:
        profile_data = rocket.get_user_info(username=username)
        return jsonify(profile_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Define a route for scraping Instagram posts data
@app.route('/scrape/posts', methods=['GET'])
def scrape_posts():
    userid = request.args.get('userid')
    print(userid)
    if not userid:
        return jsonify({'error': 'Userid parameter is required'}), 400
    
    try:
        posts_data = rocket.get_user_clips(userid,count=10)
        return jsonify(posts_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
