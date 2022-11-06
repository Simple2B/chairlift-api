import asyncio
from asyncio import StreamReader, StreamWriter
from .schema import ServerConfig


class TCPServer:
    def __init__(self, config: ServerConfig):
        self.config = config

    async def connect(self, reader: StreamReader, writer: StreamWriter) -> None:
        raise NotImplementedError

    async def _run(self) -> None:
        server = await asyncio.start_server(self.connect, "0.0.0.0", self.config.PORT)

        # TODO replace by logger
        addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
        print(f"Serving on {addrs}")

        async with server:
            await server.serve_forever()

    def run(self) -> None:
        asyncio.run(self._run())
