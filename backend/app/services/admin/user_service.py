import random
import string

from app.models.user import User

from app.utils.database import SessionLocal

from app.services.auth_service import (
    hash_password
)

from app.services.email_service import (
    send_email
)


def generate_password():

    return ''.join(
        random.choices(
            string.ascii_letters + string.digits,
            k=10
        )
    )


def create_sub_admin(

    name: str,

    email: str,

    gender: str,

    dob: str,
):

    db = SessionLocal()

    existing = db.query(User).filter(
        User.email == email
    ).first()

    if existing:

        raise Exception(
            "User already exists"
        )

    password = generate_password()

    hashed_password = hash_password(
        password
    )

    user = User(

        name=name,

        email=email,

        password=hashed_password,

        role="sub_admin",

        is_active=True,
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    body = f"""
Hello {name},

Your Infodemiology account has been created.

Email: {email}

Password: {password}

Please login and change your password.
"""

    send_email(

        to_email=email,

        subject="Infodemiology Account",

        body=body,
    )

    return {

        "id": user.id,

        "name": user.name,

        "email": user.email,

        "role": user.role,
    }


def get_all_sub_admins():

    db = SessionLocal()

    users = db.query(User).all()

    return [

        {

            "id": u.id,

            "name": u.name,

            "email": u.email,

            "role": u.role,

            "is_active": u.is_active,
        }

        for u in users
    ]


def disable_sub_admin(user_id: int):

    db = SessionLocal()

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise Exception("User not found")

    user.is_active = False

    db.commit()

    return {"status": "disabled"}


def enable_sub_admin(user_id: int):

    db = SessionLocal()

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise Exception("User not found")

    user.is_active = True

    db.commit()

    return {"status": "enabled"}


def delete_sub_admin(user_id: int):

    db = SessionLocal()

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise Exception("User not found")

    db.delete(user)

    db.commit()

    return {"status": "deleted"}