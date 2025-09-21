from unittest.mock import AsyncMock

import pytest


@pytest.fixture
def mock_repository():
    return AsyncMock()
