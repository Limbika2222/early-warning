from firebase_admin import auth

from datetime import datetime

from app.firebase.firebase_admin import (
    firestore_db,
)

# =====================================================
# CREATE SUB ADMIN
# =====================================================

def create_sub_admin(
    name: str,
    email: str,
    gender: str,
    dob: str,
):

    # -------------------------------------------------
    # CHECK IF USER ALREADY EXISTS
    # -------------------------------------------------

    try:

        existing_user = auth.get_user_by_email(
            email
        )

        return {
            "success": False,
            "message": "User already exists",
            "uid": existing_user.uid,
            "email": email,
        }

    except:

        pass

    # -------------------------------------------------
    # TEMP PASSWORD
    # -------------------------------------------------

    temporary_password = (
        "TempPassword123!"
    )

    # -------------------------------------------------
    # CREATE FIREBASE AUTH USER
    # -------------------------------------------------

    user = auth.create_user(
        email=email,
        password=temporary_password,
        display_name=name,
        email_verified=False,
        disabled=False,
    )

    # -------------------------------------------------
    # SAVE USER PROFILE TO FIRESTORE
    # -------------------------------------------------

    firestore_db.collection(
        "users"
    ).document(
        user.uid
    ).set({

        "uid":
            user.uid,

        "name":
            name,

        "email":
            email,

        "gender":
            gender,

        "dob":
            dob,

        "role":
            "sub_admin",

        "is_active":
            True,

        "created_at":
            datetime.utcnow(),

        "last_login":
            None,
    })

    # -------------------------------------------------
    # GENERATE PASSWORD RESET LINK
    # -------------------------------------------------

    reset_link = (
        auth.generate_password_reset_link(
            email
        )
    )

    # -------------------------------------------------
    # RESPONSE
    # -------------------------------------------------

    return {

        "success":
            True,

        "message":
            "Sub admin created successfully",

        "uid":
            user.uid,

        "name":
            name,

        "email":
            email,

        "gender":
            gender,

        "dob":
            dob,

        "temporary_password":
            temporary_password,

        "reset_link":
            reset_link,
    }


# =====================================================
# GET ALL SUB ADMINS
# =====================================================

def get_all_sub_admins():

    users_ref = firestore_db.collection(
        "users"
    )

    docs = users_ref.stream()

    users = []

    for doc in docs:

        data = doc.to_dict()

        users.append({

            "uid":
                data.get("uid"),

            "name":
                data.get("name"),

            "email":
                data.get("email"),

            "gender":
                data.get("gender"),

            "dob":
                data.get("dob"),

            "role":
                data.get("role"),

            "is_active":
                data.get("is_active"),

            "created_at":
                str(
                    data.get("created_at")
                ),
        })

    return users


# =====================================================
# UPDATE SUB ADMIN
# =====================================================

def update_sub_admin(
    uid: str,
    name: str,
    gender: str,
    dob: str,
):

    firestore_db.collection(
        "users"
    ).document(
        uid
    ).update({

        "name":
            name,

        "gender":
            gender,

        "dob":
            dob,
    })

    return {
        "success": True,
        "message": "User updated successfully",
    }


# =====================================================
# DISABLE SUB ADMIN
# =====================================================

def disable_sub_admin(
    uid: str,
):

    auth.update_user(
        uid,
        disabled=True,
    )

    firestore_db.collection(
        "users"
    ).document(
        uid
    ).update({

        "is_active":
            False,
    })

    return {
        "success": True,
        "message": "User disabled successfully",
    }


# =====================================================
# ENABLE SUB ADMIN
# =====================================================

def enable_sub_admin(
    uid: str,
):

    auth.update_user(
        uid,
        disabled=False,
    )

    firestore_db.collection(
        "users"
    ).document(
        uid
    ).update({

        "is_active":
            True,
    })

    return {
        "success": True,
        "message": "User enabled successfully",
    }


# =====================================================
# DELETE SUB ADMIN
# =====================================================

def delete_sub_admin(
    uid: str,
):

    try:

        # ---------------------------------------------
        # DELETE FIREBASE AUTH USER
        # ---------------------------------------------

        auth.delete_user(uid)

    except Exception as e:

        print(
            "AUTH DELETE ERROR:",
            str(e)
        )

    try:

        # ---------------------------------------------
        # DELETE FIRESTORE DOCUMENT
        # ---------------------------------------------

        firestore_db.collection(
            "users"
        ).document(
            uid
        ).delete()

    except Exception as e:

        print(
            "FIRESTORE DELETE ERROR:",
            str(e)
        )

    return {

        "success": True,

        "message":
            "User deleted successfully",
    }

# =====================================================
# SEND PASSWORD RESET
# =====================================================

def send_password_reset(
    email: str,
):

    reset_link = (
        auth.generate_password_reset_link(
            email
        )
    )

    return {

        "success": True,

        "message":
            "Password reset link generated",

        "reset_link":
            reset_link,
    }
