import gzip
import struct

import httpx
import pytest


@pytest.mark.asyncio
async def test_id(asgi_client: httpx.AsyncClient):
    response = await asgi_client.get("/api/hitomi/id")
    assert response.status_code == 200
    ids = list(struct.unpack(f"<{len(response.content) // 4}I", response.content))
    assert ids[0] == 2639954
