# from jose import jwt
# from datetime import datetime, timedelta

# SECRET_KEY = "mysecretkeyexample"
# ALGORITHM = "HS256"

# def create_token(data: dict):
#     expire = datetime.utcnow() + timedelta(hours=2)
#     data.update({"exp": expire})
#     return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)






# from fastapi import Depends, HTTPException
# from fastapi.security import OAuth2PasswordBearer
# from jose import jwt, JWTError

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# SECRET_KEY = "mysecretkey"   # use a long secret key in real project
# ALGORITHM = "HS256"

# def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")

#         if username is None:
#             raise HTTPException(status_code=401, detail="Invalid credentials")

#         return {"username": username}
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid or Expired Token")



# from datetime import datetime, timedelta
# from jose import jwt

# SECRET_KEY = "your_secret_key"
# ALGORITHM = "HS256"

# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()

#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=30)

#     to_encode.update({"exp": expire})

#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "my_super_secret_key_12345"   # Single key
ALGORITHM = "HS256"

def create_token(data: dict):
    expire = datetime.utcnow() + timedelta(hours=2)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
