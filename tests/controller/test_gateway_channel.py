import pytest
from tests.fixture.gateway_channel import GatewayTCPClient
from struct import pack


@pytest.mark.asyncio
async def test_gateway_channel(gateway_client: GatewayTCPClient):
    recv = await gateway_client.send_data(pack("H", 5))
    assert recv
