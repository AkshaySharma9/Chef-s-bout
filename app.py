from flask import Flask, redirect, request, session, url_for
from flask_session import Session
import requests
from tempfile import mkdtemp

from codechef_api import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
@login_required
def index():
	""" Show logged in user the welcome page """

	return render_template("index.html")

@app.route("/login")
def login():
	"""Log user in."""

    # forget any user_id

    #session.clear()

	# to get the access token if authorization code is present
	if "code" in request.args:
		authorization_code = request.args.get("code")

		# making the curl request
		json = '{"grant_type": "authorization_code","code": "' + authorization_code + '","client_id":"' + client_id + '","client_secret":"' + client_secret + '","redirect_uri":"' + redirect_uri + '"}'

		headers = {'content-Type': 'application/json'}

		response = (requests.post("https://api.codechef.com/oauth/token", data=json, headers=headers).json())['result']['data']

		# updating the tokens
		access_token = response['access_token']
		refresh_token = response['refresh_token']

		# getting the name of user and saving it
		session["user_id"] = get_user_details(response['access_token'])['content']['username']

		return redirect(url_for("index"))

	# get the authorization code first
	else:
		url = 'https://api.codechef.com/oauth/authorize?response_type=code&client_id=' + client_id + '&redirect_uri=' + redirect_uri +'&state=xyz'

	    # redirect to codechef login page
		return redirect(url)

