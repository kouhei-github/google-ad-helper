from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from mangum import Mangum
from routes.index import (
    auth,
    health_check,
    user,
)

from config.index import Base, engine

app = FastAPI()

# add Cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

handler = Mangum(app)

app.include_router(auth)
app.include_router(health_check)
app.include_router(user)
