import os
import json

import firebase_admin

from firebase_admin import (
    credentials,
    firestore,
)

from dotenv import load_dotenv

# =====================================================
# LOAD ENV VARIABLES
# =====================================================

load_dotenv()

# =====================================================
# GET FIREBASE JSON FROM ENV
# =====================================================

firebase_json = os.getenv(
    "FIREBASE_SERVICE_ACCOUNT"
)

# =====================================================
# VALIDATE ENV
# =====================================================

if not firebase_json:

    raise Exception(
        "FIREBASE_SERVICE_ACCOUNT missing from .env"
    )

# =====================================================
# CONVERT JSON STRING TO DICTIONARY
# =====================================================

firebase_dict = json.loads(
    firebase_json
)

# =====================================================
# FIREBASE CREDENTIALS
# =====================================================

cred = credentials.Certificate(
    firebase_dict
)

# =====================================================
# INITIALIZE FIREBASE APP
# =====================================================

if not firebase_admin._apps:

    firebase_admin.initialize_app(
        cred
    )

# =====================================================
# FIRESTORE CLIENT
# =====================================================

firestore_db = firestore.client()

# =====================================================
# SUCCESS MESSAGE
# =====================================================

print(
    "🔥 Firebase Admin Initialized"
)
