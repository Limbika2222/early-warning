from fastapi import (
    APIRouter,
    HTTPException,
)

from pydantic import BaseModel

from app.services.admin.user_service import (

    create_sub_admin,

    get_all_sub_admins,

    disable_sub_admin,

    enable_sub_admin,

    delete_sub_admin,
)

from app.services.email_service import (
    send_email
)

# =====================================================
# ROUTER
# =====================================================

router = APIRouter(

    prefix="/api/admin",

    tags=["Admin"],
)

# =====================================================
# REQUEST MODELS
# =====================================================

class CreateUserRequest(
    BaseModel
):

    name: str

    email: str

    gender: str

    dob: str


class ResetPasswordRequest(
    BaseModel
):

    email: str

# =====================================================
# CREATE USER
# =====================================================

@router.post(
    "/create-user"
)
def create_user(

    payload: CreateUserRequest
):

    try:

        result = create_sub_admin(

            name=payload.name,

            email=payload.email,

            gender=payload.gender,

            dob=payload.dob,
        )

        return {

            "success": True,

            "message":
                "Sub admin created successfully",

            "user": result,
        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e),
        )

# =====================================================
# GET USERS
# =====================================================

@router.get(
    "/users"
)
def get_users():

    try:

        users = get_all_sub_admins()

        return {

            "success": True,

            "users": users,
        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e),
        )

# =====================================================
# DISABLE USER
# =====================================================

@router.patch(
    "/disable/{uid}"
)
def disable_user(
    uid: int
):

    try:

        result = disable_sub_admin(
            uid
        )

        return {

            "success": True,

            "message":
                "User disabled successfully",

            "data": result,
        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e),
        )

# =====================================================
# ENABLE USER
# =====================================================

@router.patch(
    "/enable/{uid}"
)
def enable_user(
    uid: int
):

    try:

        result = enable_sub_admin(
            uid
        )

        return {

            "success": True,

            "message":
                "User enabled successfully",

            "data": result,
        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e),
        )

# =====================================================
# DELETE USER
# =====================================================

@router.delete(
    "/delete/{uid}"
)
def delete_user(
    uid: int
):

    try:

        result = delete_sub_admin(
            uid
        )

        return {

            "success": True,

            "message":
                "User deleted successfully",

            "data": result,
        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e),
        )

# =====================================================
# RESET PASSWORD EMAIL
# =====================================================

@router.post(
    "/reset-password"
)
def reset_password(

    payload: ResetPasswordRequest
):

    try:

        send_email(

            to_email=payload.email,

            subject="Password Reset",

            body="""
Please contact the administrator
to reset your password.
""",
        )

        return {

            "success": True,

            "message":
                "Password reset email sent",
        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e),
        )