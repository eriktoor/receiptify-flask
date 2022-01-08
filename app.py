from flask import Flask, request, url_for, session, redirect, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time 
from time import gmtime, strftime
from credentials import CLIENT_ID, CLIENT_SECRET, SECRET_KEY
import os

# Defining consts
TOKEN_CODE = "token_info"
MEDIUM_TERM = "medium_term"
SHORT_TERM = "short_term"
LONG_TERM = "long_term"

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=url_for("redirectPage",_external=True), 
        scope="user-top-read user-library-read"
    )

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['SESSION_COOKIE_NAME'] = 'Eriks Cookie'

@app.route('/')
def index():
    name = 'username'
    return render_template('index.html', title='Welcome', username=name)

@app.route('/login')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear() 
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_CODE] = token_info    
    return redirect(url_for("getTracks", _external=True))


def get_token(): 
    token_info = session.get(TOKEN_CODE, None)
    if not token_info: 
        raise "exception"
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60 
    if (is_expired): 
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info 

@app.route('/getTracks')
def getTracks():
    try: 
        token_info = get_token()
    except: 
        print("user not logged in")
        return redirect("/")
    sp = spotipy.Spotify(
        auth=token_info['access_token'],
    )

    current_user_name = sp.current_user()['display_name']
    short_term = sp.current_user_top_tracks(
        limit=10,
        offset=0,
        time_range=SHORT_TERM,
    )
    medium_term = sp.current_user_top_tracks(
        limit=10,
        offset=0,
        time_range=MEDIUM_TERM,
    )
    long_term = sp.current_user_top_tracks(
        limit=10,
        offset=0,
        time_range=LONG_TERM,
    )

    if os.path.exists(".cache"): 
        os.remove(".cache")

    return render_template('receipt.html', user_display_name=current_user_name, short_term=short_term, medium_term=medium_term, long_term=long_term, currentTime=gmtime())


@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    return strftime("%a, %d %b %Y", date)

@app.template_filter('mmss')
def _jinja2_filter_miliseconds(time, fmt=None):
    time = int(time / 1000)
    minutes = time // 60 
    seconds = time % 60 
    if seconds < 10: 
        return str(minutes) + ":0" + str(seconds)
    return str(minutes) + ":" + str(seconds ) 