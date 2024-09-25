from typing import List
from fastapi import APIRouter

router = APIRouter(tags=["test"])


@router.get("/test")
async def tests():
    return "test"
