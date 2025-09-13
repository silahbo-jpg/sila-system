"""
BI (Bilhete de Identidade) Issuance Routes.

This module contains the API routes for BI issuance functionality.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db

router = APIRouter()

@router.get("/emissao-bi", status_code=status.HTTP_200_OK)
async def emissao_bi():
    """
    BI issuance endpoint.
    
    Returns:
        dict: A simple message indicating the route is working.
    """
    return {"message": "BI issuance route is working!"}
