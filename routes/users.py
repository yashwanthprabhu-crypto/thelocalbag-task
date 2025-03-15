from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Dict
from models import User, UserCreate, UserResponse

router = APIRouter()

# In-memory storage
users_db: Dict[int, dict] = {}

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    if user.id in users_db:
        raise HTTPException(status_code=400, detail="User ID already exists")
    
    # Check for duplicate phone number
    if any(u["phone_no"] == user.phone_no for u in users_db.values()):
        raise HTTPException(status_code=400, detail="Phone number already registered")
    
    users_db[user.id] = user.dict()
    return {"message": "User created successfully"}

@router.get("/", response_model=List[User])
async def get_users():
    return list(users_db.values())

@router.get("/search/by-name", response_model=List[User])
async def search_users(name: str = Query(..., min_length=2)):
    if not name.strip():
        raise HTTPException(status_code=400, detail="Search name cannot be empty")
    return [user for user in users_db.values() if name.lower() in user["name"].lower()]

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="User ID must be a positive integer")
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserCreate):
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="User ID must be a positive integer")
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check for duplicate phone number, excluding current user
    if any(u["phone_no"] == user_update.phone_no and u["id"] != user_id for u in users_db.values()):
        raise HTTPException(status_code=400, detail="Phone number already registered to another user")
    
    user_data = user_update.dict()
    user_data["id"] = user_id
    users_db[user_id] = user_data
    return {"message": "User updated successfully"}

@router.delete("/{user_id}", response_model=UserResponse)
async def delete_user(user_id: int):
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="User ID must be a positive integer")
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    del users_db[user_id]
    return {"message": "User deleted successfully"}