# from pydantic import BaseModel

# class UserCreate(BaseModel):
#     username: str
#     email: str
#     password: str

from pydantic import BaseModel, EmailStr, Field, validator
import re

class UserCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    username: str
    password: str = Field(..., min_length=8)

    @validator("password")
    def validate_password(cls, value):
        password_pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&]).+$'
        if not re.match(password_pattern, value):
            raise ValueError(
                "Password must contain at least 1 uppercase, 1 lowercase, 1 number and 1 special character"
            )
        return value


class UserLogin(BaseModel):
    username: str
    password: str

class StaffCreate(BaseModel):
    name: str
    role: str
    contact: str

class StaffResponse(BaseModel):
    id: int
    name: str
    role: str
    contact: str

    class Config:
        orm_mode = True


from pydantic import BaseModel, EmailStr, Field

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)
    
# from pydantic import BaseModel

# class ResetPasswordRequest(BaseModel):
#     token: str
#     new_password: str
    
