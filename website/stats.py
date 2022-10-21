from flask import Blueprint, render_template, redirect, session
from dotenv import load_dotenv
import os
import requests

load_dotenv()

stats = Blueprint('stats', __name__)

base_api_url = "https://api.twitch.tv/helix/"

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

def refreshToken():
    refresh = requests.post("https://id.twitch.tv/oauth2/token--data-urlencode?grant_type=refresh_token&refresh_token="+os.getenv('REFRESH_TOKEN')+"&client_id="+client_id+"&client_secret="+client_secret)
    requests.post("https://id.twitch.tv/oauth2/revoke?client_id="+client_id+"&token="+os.getenv('ACCESS_TOKEN'))
    if(refresh.status_code == 400):
        return redirect('/login')
    data = refresh.json()
    os.environ['ACCESS_TOKEN'] = data['access_token']
    os.environ['REFRESH_TOKEN'] = data['access_token']

def validateRequest():
    resp = (requests.get("https://id.twitch.tv/oauth2/validate", headers={'Authorization': 'Bearer '+os.getenv('ACCESS_TOKEN')})).json()
    return resp

@stats.route('/dashboard')
def dashboard():
    try:
        r = requests.get(base_api_url+"users", params={'login': 'twitchdev'}, headers={'Authorization': 'Bearer '+os.getenv('ACCESS_TOKEN'), 'Client-Id': client_id})
        if(r.status_code == 401):
            refreshToken()
    except:
        if 'ACCESS_TOKEN' in os.environ:
            refreshToken()
        else:
            return redirect('/login')
    else:
        validation = validateRequest()
        login = validation['login']
        user_id = validation['user_id']
        #stream stats
        latest_stream = (requests.get(base_api_url+"videos", params={'user_id': '125957227'}, headers={'Authorization': 'Bearer '+os.getenv('ACCESS_TOKEN'), 'Client-Id': client_id})).json()

        #b_l = (requests.get(base_api_url+"bits/leaderboard", headers={'Authorization': 'Bearer '+os.getenv('ACCESS_TOKEN'), 'Client-Id': os.getenv('CLIENT_ID')})).json()
        #c_r_e = (requests.get(base_api_url+"channels/editors", params={'broadcaster_id': '192742414'}, headers={'Authorization': 'Bearer '+os.getenv('ACCESS_TOKEN'), 'Client-Id': os.getenv('CLIENT_ID')})).json()
        #c_r_g = (requests.get(base_api_url+"goals", params={'broadcaster_id': '192742414'}, headers={'Authorization': 'Bearer '+os.getenv('ACCESS_TOKEN'), 'Client-Id': os.getenv('CLIENT_ID')})).json()
        #c_r_p = (requests.get(base_api_url+"bits/leaderboard", params={'broadcaster_id': '192742414'}, headers={'Authorization': 'Bearer '+os.getenv('ACCESS_TOKEN'), 'Client-Id': os.getenv('CLIENT_ID')})).json()
        
        
        return render_template('home.html', ls=latest_stream)
    