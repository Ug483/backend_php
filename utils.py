from bcrypt import hashpw, gensalt, checkpw

def hash_password(password: str) -> str:
    return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

def verify_password(plain: str, hashed: str) -> bool:
    return checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))
