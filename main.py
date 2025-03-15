from fastapi import FastAPI
from routes.users import router as users_router

app = FastAPI()

# Include user routes
app.include_router(users_router, prefix="/users", tags=["users"])