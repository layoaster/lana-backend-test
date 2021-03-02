"""
API router configuration for the API version 1.
"""
from fastapi import APIRouter

from lana_store.api.v1.endpoints import carts


api_router = APIRouter()

api_router.include_router(carts.router, prefix="/carts", tags=["carts"])
