from flask import Blueprint, render_template, redirect, url_for, request, session
from flask import current_app as app
from website import get_endpoint
from dotenv import load_dotenv
import os
import requests
from authlib.integrations.flask_client import OAuth

load_dotenv()

auth = Blueprint('auth', __name__)

endpoint = get_endpoint()

oauth = OAuth(app)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html", ep = endpoint)

@auth.route('/twitch', methods=['GET', 'POST'])
def twitch():
    oauth.register(
        name="twitch",
        client_id=os.getenv('CLIENT_ID'),
        client_secret=os.getenv('CLIENT_SECRET'),
        authorize_url="https://id.twitch.tv/oauth2/authorize",
        access_token_url="https://id.twitch.tv/oauth2/token",
        api_base_url="https://api.twitch.tv/helix/",
        client_kwargs={
            'redirect_uri':'http://localhost:5000/twitch/auth',
            'response_type': 'code',
            'scope' : 'bits:read channel:read:editors channel:read:goals channel:read:polls channel:read:predictions channel:read:hype_train channel:read:redemptions channel:read:subscriptions moderator:read:chat_settings moderator:read:blocked_terms moderation:read user:read:email user:read:broadcast user:read:follows user:read:blocked_users user:read:subscriptions',
            'force_verify': 'true'
        }
    )
    redirect_uri = url_for('.twitch_auth', _external=True)
    return oauth.twitch.authorize_redirect(redirect_uri)

@auth.route('/twitch/auth', methods=['GET', 'POST'])
def twitch_auth():
    logged_in=True
    q = request.args
    code = q['code']

    atu = "https://id.twitch.tv/oauth2/token"
    params = {
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://localhost:5000/twitch/auth'
    }

    p = requests.post(atu, params)
    access_token = p.json()['access_token']
    refresh_token = p.json()['refresh_token']

    os.environ['ACCESS_TOKEN'] = access_token
    os.environ['REFRESH_TOKEN'] = refresh_token


    return redirect('/dashboard')