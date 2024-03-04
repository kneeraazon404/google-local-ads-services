import os
import json
import datetime
import logging
import requests
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
)
from flask_migrate import Migrate
from oauthlib.oauth2 import WebApplicationClient
from dotenv import load_dotenv

# Load environment variables from .env file for security and convenience
load_dotenv()

# Configure logging to output to stdout, enhancing visibility of application processes
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# OAuth2 credentials and setup for Google Sign-In integration
GOOGLE_CLIENT_ID = (
    "19654420609-tghnn2tspr24o2db817lerdvq35pqssv.apps.googleusercontent.com"
)
GOOGLE_CLIENT_SECRET = "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"
SCOPE = ["openid", "email", "profile", "https://www.googleapis.com/auth/adwords"]
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# Initialize Flask application with configurations for database and secret key
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///database.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))

# Initialize database, migration tool, login manager, and OAuth2 client
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
client = WebApplicationClient(GOOGLE_CLIENT_ID)


# User model representing an authenticated user with tokens for Google API access
class User(UserMixin, db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    profile_pic = db.Column(db.String(250), nullable=True)
    access_token = db.Column(db.String(250), nullable=True)
    refresh_token = db.Column(db.String(250), nullable=True)
    token_expiry = db.Column(db.DateTime, nullable=True)

    def save_tokens(self, access_token, refresh_token, token_expiry):
        # Update user's OAuth tokens and expiry, then commit changes to the database
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_expiry = token_expiry
        db.session.commit()
        logging.info(f"Tokens updated for user: {self.id}")


# Flask-Login loader callback to reload user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Home route displays all users with access to Google Ads data
@app.route("/")
def index():
    logging.info("Accessing the index page")
    users_with_access = User.query.filter(User.access_token.isnot(None)).all()
    ads_data = []

    for user in users_with_access:
        # Fetch Google Ads data for each user
        user_ads = access_google_ads_api(user.id)
        ads_data.append(
            {
                "user_id": user.id,
                "name": user.name,
                "email": user.email,
                "ads": user_ads if user_ads else "No ads data available.",
            }
        )

    return render_template("index.html", ads_data=ads_data)


# Login route initiates OAuth2 flow with Google
@app.route("/login")
def login():
    logging.info("Initiating login process")
    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    request_uri = client.prepare_request_uri(
        authorization_endpoint, redirect_uri=request.base_url + "/callback", scope=SCOPE
    )
    return redirect(request_uri)


# Callback route completes the OAuth2 flow, retrieving user information and tokens
@app.route("/login/callback")
def callback():
    code = request.args.get("code")
    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )
    tokens = token_response.json()
    client.parse_request_body_response(json.dumps(tokens))
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    userinfo = userinfo_response.json()

    if userinfo.get("email_verified"):
        unique_id = userinfo["sub"]
        users_email = userinfo.get("email")
        picture = userinfo.get("picture")
        users_name = userinfo.get("given_name")
        user = User.query.get(unique_id)

        if not user:
            user = User(
                id=unique_id, name=users_name, email=users_email, profile_pic=picture
            )
            db.session.add(user)
            logging.info(f"New user created: {unique_id}")

        refresh_token = tokens.get(
            "refresh_token", user.refresh_token if user else None
        )

        user.save_tokens(
            access_token=tokens["access_token"],
            refresh_token=refresh_token,
            token_expiry=datetime.datetime.utcnow()
            + datetime.timedelta(seconds=tokens["expires_in"]),
        )

        db.session.commit()
        login_user(user)
        logging.info(f"User logged in: {unique_id}")
        return redirect(url_for("index"))
    else:
        logging.error("User email not verified by Google")
        return "User email not available or not verified by Google.", 400


# Logout route logs the user out
@app.route("/logout")
@login_required
def logout():
    logout_user()
    logging.info("User logged out")
    return redirect(url_for("index"))


# Function to refresh Google Ads API access token
def refresh_access_token(refresh_token):
    logging.info("Refreshing access token")
    refresh_url = "https://oauth2.googleapis.com/token"
    payload = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }
    response = requests.post(refresh_url, data=payload)
    if response.status_code == 200:
        logging.info("Access token refreshed successfully")
    else:
        logging.error("Failed to refresh access token")
    return response.json() if response.status_code == 200 else None


# Function to access Google Ads API with refreshed token
def access_google_ads_api(user_id):
    logging.info(f"Accessing Google Ads API for user: {user_id}")
    user = User.query.get(user_id)
    if not user:
        logging.error(f"User {user_id} not found.")
        return []

    if datetime.datetime.utcnow() >= user.token_expiry:
        logging.info(f"Token for user {user_id} is expired. Refreshing token.")
        refresh_response = refresh_access_token(user.refresh_token)
        if refresh_response:
            user.save_tokens(
                refresh_response["access_token"],
                refresh_response.get("refresh_token", user.refresh_token),
                datetime.datetime.utcnow()
                + datetime.timedelta(seconds=refresh_response["expires_in"]),
            )
            db.session.commit()
            logging.info("Token refreshed successfully")
        else:
            logging.error("Failed to refresh token for Google Ads API access")
            return []

    # Example functionality placeholder for accessing Google Ads data
    google_ads_api_version = "v8"
    customer_id = "INSERT_CUSTOMER_ID_HERE"  # Placeholder for actual customer ID
    google_ads_api_url = f"https://googleads.googleapis.com/{google_ads_api_version}/customers/{customer_id}/campaigns"
    headers = {
        "Authorization": f"Bearer {user.access_token}",
        "developer-token": os.environ.get("GOOGLE_ADS_DEVELOPER_TOKEN"),
        "login-customer-id": customer_id,
    }
    response = requests.get(google_ads_api_url, headers=headers)

    if response.status_code == 200:
        logging.info(f"Successfully retrieved campaigns for user: {user_id}")
        campaigns_data = response.json().get("campaigns", [])
        return campaigns_data
    else:
        logging.error(
            f"Failed to retrieve campaigns for user {user_id}: {response.text}"
        )
        return []


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure database tables are created
        logging.info("Database tables created")

    app.run(ssl_context="adhoc", port=5001, debug=True)
