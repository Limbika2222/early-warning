from datetime import (
    datetime,
    timedelta,
)

from jose import jwt

from passlib.context import (
    CryptContext,
)

from app.models.user import User

from app.utils.database import (
    SessionLocal,
)

SECRET_KEY = (
    "SUPER_SECRET_KEY_123"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

pwd_context = CryptContext(

    schemes=["bcrypt"],

    deprecated="auto",
)


def hash_password(
    password: str
):

    return pwd_context.hash(
        password
    )


def verify_password(

    plain_password: str,

    hashed_password: str
):

    return pwd_context.verify(

        plain_password,

        hashed_password,
    )


def authenticate_user(

    email: str,

    password: str
):

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:

        return None

    if not verify_password(

        password,

        user.password
    ):

        return None

    return user


def create_access_token(
    data: dict
):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=
        ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update(
        {"exp": expire}
    )

    encoded_jwt = jwt.encode(

        to_encode,

        SECRET_KEY,

        algorithm=ALGORITHM,
    )

    return encoded_jwt