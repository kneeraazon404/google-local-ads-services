# Flask Google Login Example

This project demonstrates how to implement Google OAuth 2.0 authentication in a Flask application. It utilizes Flask-Login for session management and requests OAuthLib for OAuth 2 client setup. The example includes user authentication via Google, creating a simple user session, and handling login and logout functionalities.

## Features

- Google OAuth 2.0 authentication
- User session management using Flask-Login
- SQLite database for storing user data
- User profile page that displays basic user information

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
