"""
The API views for the `Cart` resource on the version `v1`.
"""
from fastapi import APIRouter


router = APIRouter()


@router.get("/")
async def cart_hello():
    return {"message": "Hello World"}
