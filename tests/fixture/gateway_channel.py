import time
import pytest_asyncio
import asyncio
from functools import lru_cache
from typing import AsyncIterator
from multiprocessing import Process
from app.controller import GatewayChannel
from app.controller.tcp_server.schema import ServerConfig
from app.config import Settings
from tests.conftest import get_test_settings


class GatewayTCPClient:
    def __init__(self, conf: ServerConfig):
        self.conf = conf

    async def send_data(self, data: bytes) -> bytes:
        reader, writer = await asyncio.open_connection("127.0.0.1", self.conf.PORT)
        writer.write(data)
        await writer.drain()

        data = await reader.read(100)
        writer.close()
        return data


SETTINGS_MAP: dict = {
    "GW_TCP_SERVER_PORT": "PORT",
}


@lru_cache
def get_tcp_server_config() -> ServerConfig:
    settings: Settings = get_test_settings()

    server_config_data = {}
    for mapped_attr, attr in SETTINGS_MAP.items():
        server_config_data[attr] = getattr(settings, mapped_attr)

    return ServerConfig(**server_config_data)


def start_gw_tcp_server() -> None:
    sc: ServerConfig = get_tcp_server_config()
    gt_channel: GatewayChannel = GatewayChannel(sc)
    gt_channel.run()


@pytest_asyncio.fixture
async def gateway_client() -> AsyncIterator[GatewayTCPClient]:
    sc: ServerConfig = get_tcp_server_config()

    # Start gateway channel
    tcp_gw_server_proc: Process = Process(target=start_gw_tcp_server)
    tcp_gw_server_proc.start()

    gw_channel_client = GatewayTCPClient(sc)

    # Wait till server up
    server_started = False
    for i in range(3):
        try:
            _, writer = await asyncio.open_connection("127.0.0.1", sc.PORT)
            server_started = True
            writer.close()
            break
        except IOError:
            time.sleep(1)

    if not server_started:
        tcp_gw_server_proc.join()
        raise TimeoutError

    # Return TCP client and kill TCP server after test
    try:
        yield gw_channel_client
    finally:
        tcp_gw_server_proc.kill()
