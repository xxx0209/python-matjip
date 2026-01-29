# app/services/place_service.py

import httpx
from app.config import KAKAO_API_KEY

async def search_places(location: str, food: str, lat: float, lng: float):
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"

    headers = {
        "Authorization": f"KakaoAK {KAKAO_API_KEY}"
    }

    query = f"{location or ''} {food or ''}".strip()
    if not query:
        return []

    params = {
        "query": query,
        "category_group_code": "FD6",
        "x": lng,
        "y": lat,
        "radius": 2000,
        "sort": "distance",
        "size": 10
    }

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            res = await client.get(url, headers=headers, params=params)

        res.raise_for_status()
        data = res.json()

    except Exception as e:
        print("카카오 API 오류:", e)
        return []

    places = [
        {
            "name": p.get("place_name"),
            "address": p.get("road_address_name") or p.get("address_name"),
            "lat": p.get("y"),
            "lng": p.get("x"),
            "category": p.get("category_name"),
            "distance": p.get("distance")
        }
        for p in data.get("documents", [])
    ]

    return places
