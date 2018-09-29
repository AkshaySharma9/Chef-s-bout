from functools import wraps
from flask import redirect, render_template, request, session
import requests

# fields required to access codechef api
global config
config = {
        'client_id' : 'e5e9dbf414ac2a401100e8802cad7fed',
        'client_secret' : '8f6e5771f63c12caa98e8c1857930ced',
        'redirect_uri' : 'http://workspace-a09akshay09.cs50.io:8080/login'
    }


def login_required(f):
    """
    Decorate routes to require login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def get_user_details():
    s = 'Bearer ' + config['access_token']

    headers = {'Accept': 'application/json', 'Authorization' :  str(s)}

    response = (requests.get("https://api.codechef.com/users/me", headers=headers)).json()

    return response['result']['data']