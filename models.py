from pydantic import BaseModel, Field, validator
import re

class UserBase(BaseModel):
    id: int = Field(..., gt=0)
    name: str = Field(..., min_length=2, max_length=50)
    phone_no: str = Field(..., min_length=10, max_length=15)
    address: str = Field(..., min_length=5, max_length=200)

    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty or whitespace')
        if not re.match(r'^[a-zA-Z\s-]+$', v):
            raise ValueError('Name can only contain letters, spaces, and hyphens')
        return v.strip()

    @validator('phone_no')
    def validate_phone(cls, v):
        if not re.match(r'^\+?[1-9]\d{9,14}$', v):
            raise ValueError('Invalid phone number format')
        return v

    @validator('address')
    def validate_address(cls, v):
        if not v.strip():
            raise ValueError('Address cannot be empty or whitespace')
        return v.strip()

class UserCreate(UserBase):
    pass

class User(UserBase):
    pass

class UserResponse(BaseModel):
    message: str