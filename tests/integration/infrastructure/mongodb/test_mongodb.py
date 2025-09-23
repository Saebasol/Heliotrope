from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest

from heliotrope.infrastructure.mongodb import MongoDB


@pytest.mark.asyncio
async def test_create_mongodb_with_atlas():
    atlas_url = "mongodb+srv://user:pass@cluster.mongodb.net"
    mongodb = await MongoDB.create(atlas_url)

    assert isinstance(mongodb, MongoDB)
    assert mongodb.client is not None
    assert mongodb.is_atlas is True
    assert mongodb.collection is not None


@pytest.mark.asyncio
async def test_create_mongodb_without_atlas():
    regular_url = "mongodb://localhost:27017"

    mongodb = await MongoDB.create(regular_url)
    assert isinstance(mongodb, MongoDB)
    assert mongodb.client is not None
    assert mongodb.is_atlas is False
    assert mongodb.collection is not None
