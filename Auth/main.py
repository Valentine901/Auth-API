from fastapi import FastAPI 
from endpoint import router
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
app.include_router(router)
app.add_middleware(
    CORSMiddleware, 
    allow_origins = ['http://localhost:5173', "http://localhost:5174", "http://localhost:3000"],
    allow_credentials=True, 
    allow_headers=["*"],
    allow_methods=["*"]
)