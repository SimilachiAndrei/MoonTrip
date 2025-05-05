from flask import Flask, session, redirect, url_for, request, render_template, flash
from flask_session import Session
import msal
import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
Session(app)

# Azure AD B2C Configuration
B2C_TENANT = os.getenv("B2C_TENANT")
B2C_CLIENT_ID = os.getenv("B2C_CLIENT_ID")
B2C_CLIENT_SECRET = os.getenv("B2C_CLIENT_SECRET")
B2C_POLICY = os.getenv("B2C_POLICY", "B2C_1_signupsignin1")
B2C_AUTHORITY = f"https://{B2C_TENANT}.b2clogin.com/{B2C_TENANT}.onmicrosoft.com/{B2C_POLICY}"
B2C_SCOPE = [f"https://{B2C_TENANT}.onmicrosoft.com/api/user_impersonation"]
REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:5000/auth/callback")

# Initialize MSAL app
msal_app = msal.ConfidentialClientApplication(
    client_id=B2C_CLIENT_ID,
    client_credential=B2C_CLIENT_SECRET,
    authority=B2C_AUTHORITY
)

@app.route('/')
def index():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template('index.html', user=session["user"])

@app.route('/login')
def login():
    # Generate the auth URL with state parameter for security
    state = os.urandom(16).hex()
    session["state"] = state
    
    auth_url = msal_app.get_authorization_request_url(
        scopes=B2C_SCOPE,
        redirect_uri=REDIRECT_URI,
        state=state
    )
    return redirect(auth_url)

@app.route('/auth/callback')
def auth_callback():
    # Verify state parameter to prevent CSRF
    if request.args.get('state') != session.get("state"):
        flash("Invalid state parameter. Possible CSRF attack.", "error")
        return redirect(url_for("index"))
    
    if request.args.get('error'):
        error = request.args.get('error')
        error_description = request.args.get('error_description', 'No description provided')
        flash(f"Authentication error: {error} - {error_description}", "error")
        return redirect(url_for("index"))
    
    if request.args.get('code'):
        try:
            # Get token from auth code
            result = msal_app.acquire_token_by_authorization_code(
                code=request.args['code'],
                scopes=B2C_SCOPE,
                redirect_uri=REDIRECT_URI
            )
            
            if "error" in result:
                flash(f"Token error: {result.get('error_description')}", "error")
                return redirect(url_for("index"))
            
            # Get user info
            user_info = get_user_info(result['access_token'])
            session["user"] = user_info
            session["access_token"] = result['access_token']
            session["refresh_token"] = result.get('refresh_token')
            session["token_expires"] = datetime.now() + timedelta(seconds=result.get('expires_in', 3600))
            
            flash("Successfully logged in!", "success")
            return redirect(url_for("index"))
            
        except Exception as e:
            flash(f"Error during authentication: {str(e)}", "error")
            return redirect(url_for("index"))
    
    flash("No authorization code received", "error")
    return redirect(url_for("index"))

@app.route('/logout')
def logout():
    session.clear()
    flash("Successfully logged out!", "success")
    return redirect(url_for("index"))

def get_user_info(access_token):
    """Get user information from the access token."""
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(
            f"https://{B2C_TENANT}.b2clogin.com/{B2C_TENANT}.onmicrosoft.com/openid/userinfo",
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        app.logger.error(f"Error getting user info: {str(e)}")
        return None

@app.before_request
def check_token_expiration():
    """Check if the access token needs to be refreshed."""
    if session.get("user") and session.get("token_expires"):
        if datetime.now() >= session["token_expires"]:
            try:
                result = msal_app.acquire_token_by_refresh_token(
                    session["refresh_token"],
                    scopes=B2C_SCOPE
                )
                if "error" not in result:
                    session["access_token"] = result['access_token']
                    session["refresh_token"] = result.get('refresh_token')
                    session["token_expires"] = datetime.now() + timedelta(seconds=result.get('expires_in', 3600))
            except Exception as e:
                app.logger.error(f"Error refreshing token: {str(e)}")
                session.clear()
                return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True)
