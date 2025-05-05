from flask import Flask, session, redirect, url_for, request, render_template, flash
from flask_session import Session
import msal
import os
from dotenv import load_dotenv
import jwt  # Added for token decoding
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", os.urandom(24))
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './flask_session'  # Explicit directory
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# Initialize Session AFTER app configuration
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
    print("Session in index:", session)
    # Check if user is logged in and has valid session data
    if not all(key in session for key in ["user", "access_token", "token_expires"]):
        session.clear()
        return redirect(url_for("login"))
    
    # Check if token is expired
    token_expires_str = session.get("token_expires")
    if token_expires_str:
        token_expires = datetime.fromisoformat(token_expires_str)
        if datetime.now() >= token_expires:
            session.clear()
            return redirect(url_for("login"))
        
    return render_template('index.html', user=session["user"])


@app.route('/login')
def login():
    # Always clear the session when starting a new login
    session.clear()
    
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
    print("Session after auth:", session)
    if request.args.get('state') != session.get("state"):
        session.clear()
        flash("Invalid state parameter. Possible CSRF attack.", "error")
        return redirect(url_for("login"))
    
    if request.args.get('error'):
        session.clear()
        error = request.args.get('error')
        error_description = request.args.get('error_description', 'No description provided')
        flash(f"Authentication error: {error} - {error_description}", "error")
        return redirect(url_for("login"))
    
    if request.args.get('code'):
        try:
            result = msal_app.acquire_token_by_authorization_code(
                code=request.args['code'],
                scopes=B2C_SCOPE,
                redirect_uri=REDIRECT_URI
            )
            
            if "error" in result:
                session.clear()
                flash(f"Token error: {result.get('error_description')}", "error")
                return redirect(url_for("login"))

            # Decode ID token to get user info
            id_token = result.get("id_token")
            if not id_token:
                session.clear()
                flash("No ID token received", "error")
                return redirect(url_for("login"))

            # Decode the ID token without verification (for demo purposes)
            id_token_claims = jwt.decode(
                id_token,
                options={"verify_signature": False},
                algorithms=["RS256"]
            )

            # Store user info in session
            session["user"] = {
                "name": id_token_claims.get("name", ""),
                "email": id_token_claims.get("emails", [""])[0],
                "oid": id_token_claims.get("oid", ""),
                "given_name": id_token_claims.get("given_name", ""),
                "family_name": id_token_claims.get("family_name", "")
            }

            session["access_token"] = result['access_token']
            session["refresh_token"] = result.get('refresh_token')
            expires_at = datetime.now() + timedelta(seconds=result.get('expires_in', 3600))
            session["token_expires"] = expires_at.isoformat()

            flash("Successfully logged in!", "success")
            return redirect(url_for("index"))
            
        except Exception as e:
            session.clear()
            flash(f"Error during authentication: {str(e)}", "error")
            return redirect(url_for("login"))
    
    session.clear()
    flash("No authorization code received", "error")
    return redirect(url_for("login"))


@app.route('/logout')
def logout():
    session.clear()
    flash("Successfully logged out!", "success")
    return redirect(url_for("index"))


@app.before_request
def check_token_expiration():
    """Check if the access token needs to be refreshed."""
    # Skip token check for login-related routes and static files
    if request.endpoint in ['login', 'auth_callback', 'static', 'logout']:
        return None

    # If there's no user in session or no token_expires, clear session and redirect
    if not session.get("user") or not session.get("token_expires"):
        session.clear()
        return None

    # Check if token is expired
    if datetime.now() >= session.get("token_expires"):
        # Token is expired, try to refresh
        if session.get("refresh_token"):
            try:
                result = msal_app.acquire_token_by_refresh_token(
                    session["refresh_token"],
                    scopes=B2C_SCOPE
                )
                if "error" not in result:
                    session["access_token"] = result['access_token']
                    session["refresh_token"] = result.get('refresh_token')
                    session["token_expires"] = datetime.now() + timedelta(seconds=result.get('expires_in', 3600))
                else:
                    session.clear()
                    return redirect(url_for("login"))
            except Exception as e:
                app.logger.error(f"Error refreshing token: {str(e)}")
                session.clear()
                return redirect(url_for("login"))
        else:
            session.clear()
            return redirect(url_for("login"))

    return None


if __name__ == '__main__':
    app.run(debug=True)