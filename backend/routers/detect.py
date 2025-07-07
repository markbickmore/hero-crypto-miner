from fastapi import APIRouter, Query
from services.scanner import scan_ethereum_address

router = APIRouter()

@router.get("/detect")
def detect_tx(
    address: str = Query(..., min_length=42, max_length=42, description="ETH wallet address"),
    token: str = Query("ETH"),
    days: int = Query(7, description="How far back to search (in days)")
):
    result = scan_ethereum_address(address, token, days)
    return result