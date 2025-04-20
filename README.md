# Google Local Ads Services 🌟  
### A Flask Application for Google OAuth 2.0 Authentication and Google Ads API Integration  

This project demonstrates how to implement Google OAuth 2.0 authentication in a Flask application. It uses Flask-Login for session management, securely handles OAuth tokens, and integrates with the Google Ads API to fetch and display campaign data dynamically.

---

## ✨ Features  

- **OAuth2 Authentication**:  
  Seamlessly integrates with Google's OAuth2 for secure user authentication.  

- **Google Ads API Access**:  
  Fetches real-time Google Ads campaign data using authorized API requests.  

- **Secure Token Management**:  
  Stores access and refresh tokens securely in the database, with automatic token refresh to ensure uninterrupted API access.  

- **Dynamic Data Rendering**:  
  Displays personalized Google Ads campaign data dynamically for each authenticated user.  

- **User Session Management**:  
  Leverages Flask-Login for secure and efficient session management.  

- **Logout Functionality**:  
  Provides a secure logout option to end user sessions cleanly.  

---

## 🛠️ Requirements  

- **Python 3.x**  
- **Flask**  
- **Flask-Login**  
- **OAuthLib**  
- **SQLite**  
- **Requests**  

---

## 🔧 Installation  

1. **Clone the Repository**:  
   ```bash  
   git clone https://github.com/kneeraazon404/google-local-ads-services.git  
   cd google-local-ads-services  
   ```  

2. **Install Dependencies**:  
   Install the required Python packages:  
   ```bash  
   pip install flask flask-login oauthlib requests  
   ```  

---

## ⚙️ Configuration  

### 1. Google OAuth Credentials  
- Create a project in the [Google Developer Console](https://console.developers.google.com/).  
- Enable the Google Ads API and create credentials for a web application.  
- Obtain the `client_id` and `client_secret` values.  

### 2. Application Secret Key  
Generate a secret key for Flask to secure session cookies:  
```python  
import os  
print(os.urandom(24))  
```  

### 3. Update Configuration  
Add the following environment variables to your application:  
- `GOOGLE_CLIENT_ID`  
- `GOOGLE_CLIENT_SECRET`  
- `app.secret_key`  

---

## 🚀 Running the Application  

Start the Flask application using the following command:  
```bash  
python app.py  
```  

By default, the application runs on `https://localhost:5001`. Open this URL in your browser to test the Google login and Ads API integration.  

---

## 🎯 Usage  

1. Visit the home page: `https://localhost:5001`.  
2. Click the **Login** button to authenticate with Google.  
3. After successful authentication, view your Google profile information along with your Ads campaign data.  
4. Click the **Logout** button to securely end your session and return to the login page.  

---

## 📜 License  

This project is licensed under the MIT License. See the [LICENSE.md](LICENSE.md) file for details.  

---

## 🙏 Acknowledgments  

- [Flask Documentation](https://flask.palletsprojects.com/)  
- [Flask-Login Documentation](https://flask-login.readthedocs.io/)  
- [Google OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)  
