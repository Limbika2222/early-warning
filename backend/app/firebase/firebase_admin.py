import firebase_admin

from firebase_admin import (
    credentials,
    auth,
    firestore,
)

# =====================================================
# FIREBASE INIT
# =====================================================

cred = credentials.Certificate(
    "early-warning-dashboard-firebase-adminsdk-fbsvc-e971b35079.json"
)

if not firebase_admin._apps:

    firebase_admin.initialize_app(
        cred
    )

# =====================================================
# FIRESTORE
# =====================================================

firestore_db = firestore.client(
    database_id="users"
)

# =====================================================
# EXPORTS
# =====================================================

firebase_auth = auth