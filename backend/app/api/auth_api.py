from fastapi import APIRouter

from fastapi import HTTPException

from pydantic import BaseModel

from app.services.auth_service import (
    authenticate_user,
    create_access_token,
)

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)

class LoginRequest(
    BaseModel
):

    email: str

    password: str


@router.post("/login")
def login(
    payload: LoginRequest
):

    user = authenticate_user(

        payload.email,

        payload.password
    )

    if not user:

        raise HTTPException(

            status_code=401,

            detail="Invalid email or password",
        )

    token = create_access_token(

        {

            "sub":
                user.email
        }
    )

    return {

        "access_token":
            token,

        "token_type":
            "bearer",

        "user": {

            "id":
                user.id,

            "name":
                user.name,

            "email":
                user.email,

            "role":
                user.role,
        },
    }