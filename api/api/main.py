from fastapi import APIRouter

from api.api.routes import example

api_router = APIRouter()
api_router.include_router(example.router, prefix="/examples", tags=["examples"])
