import gzip
import struct

import httpx
import pytest


@pytest.mark.asyncio
async def test_id(asgi_client: httpx.AsyncClient):
    response = await asgi_client.get("/api/hitomi/id")
    assert response.status_code == 200
    binary = gzip.decompress(response.content)
    ids = list(struct.unpack(f"<{len(binary) // 4}I", binary))
    assert ids[0] == 2639954
