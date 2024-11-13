# Helper functions for Firebase authentication (new)
import firebase_admin
from firebase_admin import auth as firebase_auth, credentials
import os


if os.getenv("FIREBASE_SDK_CRED"):
    print(f"Firebase credentials path loaded")
else:
    raise ValueError("Firebase credentials path not found. Ensure it is set in the .env file.")

path_to_cred = os.getenv("FIREBASE_SDK_CRED")

# Initialize the Firebase Admin SDK
cred = credentials.Certificate(path_to_cred)  # Download from Firebase Console
firebase_admin.initialize_app(cred)

def verify_id_token(id_token):
    try:
        decoded_token = firebase_auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        return uid
    except Exception as e:
        print("Error verifying ID token:", e)
        return None
