from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get('/health')
def health_check():
    return {'status': 'healthy', 'service': 'reticulum-bridge'}
