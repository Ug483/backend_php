from fastapi import FastAPI, Depends, HTTPException
from database import Base, engine, get_db
from sqlalchemy.orm import Session
import models, schemas
from utils import hash_password, verify_password
from auth import create_token


from auth import SECRET_KEY, ALGORITHM, create_access_token, create_token


from schemas import ResetPasswordRequest


SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_exist = db.query(models.User).filter(models.User.username == user.username).first()
    if user_exist:
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed = hash_password(user.password)
    new_user = models.User(username=user.username, email=user.email, password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

@app.post("/login")
def login(data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == data.username).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_token({"username": user.username})
    return {"access_token": token, "token_type": "bearer"}

from schemas import StaffCreate, StaffResponse
import models
from fastapi import Depends
from sqlalchemy.orm import Session

#Add Staff
@app.post("/staff/add", response_model=StaffResponse)
def add_staff(staff: StaffCreate, db: Session = Depends(get_db)):
    new_staff = models.Staff(name=staff.name, role=staff.role, contact=staff.contact)
    db.add(new_staff)
    db.commit()
    db.refresh(new_staff)
    return new_staff

# Get All Staff
@app.get("/staff/all")
def get_all_staff(db: Session = Depends(get_db)):
    staff_list = db.query(models.Staff).all()
    return staff_list

# Update Staff
@app.put("/staff/update/{id}")
def update_staff(id: int, staff: StaffCreate, db: Session = Depends(get_db)):
    staff_data = db.query(models.Staff).filter(models.Staff.id == id).first()
    if not staff_data:
        return {"error": "Staff not found"}

    staff_data.name = staff.name
    staff_data.role = staff.role
    staff_data.contact = staff.contact
    db.commit()
    return {"message": "Staff updated successfully"}

# Delete Staff
@app.delete("/staff/delete/{id}")
def delete_staff(id: int, db: Session = Depends(get_db)):
    staff_data = db.query(models.Staff).filter(models.Staff.id == id).first()
    if not staff_data:
        return {"error": "Staff not found"}

    db.delete(staff_data)
    db.commit()
    return {"message": "Staff deleted successfully"}


# from auth import get_current_user

# @app.post("/staff/add", response_model=StaffResponse)
# def add_staff(staff: StaffCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
#     new_staff = models.Staff(name=staff.name, role=staff.role, contact=staff.contact)
#     db.add(new_staff)
#     db.commit()
#     db.refresh(new_staff)
#     return new_staff


# @app.get("/staff/all")
# def get_all_staff(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
#     return db.query(models.Staff).all()


# @app.put("/staff/update/{id}")
# def update_staff(id: int, staff: StaffCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
#     staff_data = db.query(models.Staff).filter(models.Staff.id == id).first()
#     if not staff_data:
#         return {"error": "Staff not found"}

#     staff_data.name = staff.name
#     staff_data.role = staff.role
#     staff_data.contact = staff.contact
#     db.commit()
#     return {"message": "Staff updated successfully"}


# @app.delete("/staff/delete/{id}")
# def delete_staff(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
#     staff_data = db.query(models.Staff).filter(models.Staff.id == id).first()
#     if not staff_data:
#         return {"error": "Staff not found"}

#     db.delete(staff_data)
#     db.commit()
#     return {"message": "Staff deleted successfully"}



from auth import create_access_token

@app.post("/forgot-password")
def forgot_password(request: schemas.ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")

    reset_token = create_access_token({"sub": user.email})
    
    # Optional: send token in email (later we can integrate email service)
    
    return {
        "message": "Password reset link generated successfully",
        "reset_token": reset_token  # for testing
    }

# from jose import jwt, JWTError

# @app.post("/reset-password")
# def reset_password(request: schemas.ResetPasswordRequest, db: Session = Depends(get_db)):
#     try:
#         payload = jwt.decode(request.token, SECRET_KEY, algorithms=[ALGORITHM])
#         email = payload.get("sub")

#         user = db.query(models.User).filter(models.User.email == email).first()
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")

#         user.password = pwd_context.hash(request.new_password)
#         db.commit()

#         return {"message": "Password reset successfully"}
    
#     except JWTError:
#         raise HTTPException(status_code=400, detail="Invalid or expired reset token")


from jose import jwt, JWTError
from fastapi import HTTPException, Depends

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# @app.post("/reset-password")
# def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
#     try:
#         payload = jwt.decode(request.token, SECRET_KEY, algorithms=[ALGORITHM])
#         email = payload.get("sub")

#         if email is None:
#             raise HTTPException(status_code=400, detail="Invalid token")

#         user = db.query(User).filter(User.email == email).first()
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")

#         user.password = get_password_hash(request.new_password)
#         db.commit()

#         return {"message": "Password successfully reset"}

#     except JWTError:
#         raise HTTPException(status_code=403, detail="Invalid or expired token")


@app.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    payload = jwt.decode(request.token, SECRET_KEY, algorithms=[ALGORITHM])
    email = payload.get("sub")

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    hashed_password = hash_password(request.new_password)
    user.password = hashed_password
    db.commit()

    return {"message": "Password updated successfully"}
