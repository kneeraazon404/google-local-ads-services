# Flask Google Login Example

This project demonstrates how to implement Google OAuth 2.0 authentication in a Flask application. It utilizes Flask-Login for session management and requests OAuthLib for OAuth 2 client setup. The example includes user authentication via Google, creating a simple user session, and handling login and logout functionalities.

## Features

- OAuth2 Authentication: The app integrates with Google's OAuth2 to authenticate users, granting access to Google Ads data based on their Google account credentials.

- Token Management: Stores access tokens, refresh tokens, and token expiry times in the database for each user, enabling API access on behalf of the user.

- Automatic Token Refresh: Automatically refreshes the access token using the stored refresh token when it detects the access token has expired, ensuring uninterrupted API access.

- Secure Token Storage: Utilizes Flask's environment variables and SQLAlchemy for secure storage and handling of sensitive OAuth tokens and user information.

- User Registration: Automatically registers users in the database upon successful OAuth2 authentication, storing their unique Google ID, email, name, and profile picture URL.

- User Authentication Flow: Manages the complete OAuth2 flow, from initiating the login process to handling the callback with the authorization code to retrieve tokens.

- Google Ads API Access: Uses the access token to make authorized requests to the Google Ads API, fetching campaign data for the authenticated user.

- Dynamic Content Rendering: Dynamically renders Google Ads data on the web page for each user, displaying their ads information retrieved from the Google Ads API.

- User Session Management: Leverages Flask-Login for session management, enabling secure login sessions and easy access to the user's Google Ads data during their session.

- Logout Functionality: Provides a logout route that securely logs out the user, clearing their session and redirecting them to the main page, ensuring a clean and secure end to the session.

## Requirements

- Python 3.x
- Flask
- Flask-Login
- OAuthLib
- SQLite3
- Requests

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/your-repository/flask-google-login-example.git
cd flask-google-login-example
```

Install the required Python packages:

```bash
pip install flask flask-login oauthlib requests
```

## Configuration

Before running the application, you need to configure the Google OAuth credentials and the application secret key:

1. **Google OAuth Credentials**: Create a project in the Google Developer Console, enable the Google+ API, and create credentials for a web application. You will get a `client_id` and `client_secret`.

2. **Application Secret Key**: The secret key is used by Flask to sign session cookies for protection against cookie data tampering. You can generate a secret key using Python:

   ```python
   import os
   print(os.urandom(24))
   ```

Update the `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, and `app.secret_key` in your application with the values obtained.

## Running the Application

Run the Flask application with the following command:

```bash
python app.py
```

The application will start running on `https://localhost:5001`. Navigate to this URL in your web browser to test the Google login functionality.

## Usage

- Access the home page at `https://localhost:5001`.
- Click on the "Login" button to authenticate with Google.
- After successful authentication, you will be redirected back to the home page, now displaying your Google profile name, email, and profile picture.
- Click on the "Logout" button to end the session and return to the login page.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

## Acknowledgments

- Flask documentation
- Flask-Login documentation
- Google OAuth 2.0 documentation

Please note that this README assumes you have basic knowledge of Flask and OAuth 2.0 authentication flows. Adjust the instructions as necessary for your specific environment or deployment scenario.
