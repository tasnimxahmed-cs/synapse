import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'jannatul'

    from .views import views
    from .auth import auth
    from .stats import stats

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(stats, url_prefix='/')

    return app


def get_endpoint():
    params = []
    params.append(os.getenv('CLIENT_ID'))
    params.append("http://localhost:5000/")
    params.append("token")
    params.append("bits:read channel:read:editors channel:read:goals channel:read:polls channel:read:predictions channel:read:hype_train channel:read:redemptions channel:read:subscriptions moderator:read:chat_settings moderator:read:blocked_terms moderation:read user:read:email user:read:broadcast user:read:follows user:read:blocked_users user:read:subscriptions")
    params.append("true")

    endpoint = "https://id.twitch.tv/oauth2/authorize?client_id="+os.getenv('CLIENT_ID')+"&redirect_uri=http://localhost:5000/&response_type=token&scope="+"bits:read%20channel:read:editors%20channel:read:goals%20channel:read:polls%20channel:read:predictions%20channel:read:redemptions%20channel:read:subscriptions%20moderation:read%20user:read:email%20user:read:follows%20user:read:subscriptions"+"&force_verify=true"

    return endpoint