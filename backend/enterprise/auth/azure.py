"""Azure AD OAuth stub - Enterprise feature."""
from fastapi import APIRouter

router = APIRouter(prefix="/auth/azure", tags=["authentication"])

# DON'T REGISTER THIS ROUTER IN COMMUNITY EDITION
# This file exists only for imports and type checking
# The router is never registered in main.py for community edition


@router.get("/login")
async def azure_login():
    """This should never be called (router not registered in community)."""
    pass


@router.get("/callback")
async def azure_callback():
    """This should never be called (router not registered in community)."""
    pass
