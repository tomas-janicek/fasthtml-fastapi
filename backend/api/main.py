from fastapi import APIRouter

from backend.api.routes import examples

api_router = APIRouter()
api_router.include_router(examples.router, prefix="/examples", tags=["examples"])
