import firebase_admin

from firebase_admin import (
    credentials,
    firestore,
)

# =====================================================
# FIREBASE ADMIN INITIALIZATION
# =====================================================

SERVICE_ACCOUNT_PATH = (

    "app/firebase/"
    "early-warning-dashboard-firebase-adminsdk-fbsvc-e971b35079.json"
)

cred = credentials.Certificate(
    SERVICE_ACCOUNT_PATH
)

if not firebase_admin._apps:

    firebase_admin.initialize_app(
        cred
    )

# =====================================================
# FIRESTORE
# =====================================================

firestore_db = firestore.client()

print(
    "🔥 Firebase Admin Initialized"
)