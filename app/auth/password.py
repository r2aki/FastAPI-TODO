from passlib.hash import bcrypt


def hashed_password(plain_password: str) -> str:
    return bcrypt.hash(plain_password)


def verify_password(plain_password: str, hashed_pass: str) -> bool:
    return bcrypt.verify(plain_password, hashed_pass)
