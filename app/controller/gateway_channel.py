from asyncio import StreamReader, StreamWriter
from app.controller.tcp_server import TCPServer


class GatewayChannel(TCPServer):
    async def connect(self, reader: StreamReader, writer: StreamWriter) -> None:
        # packet_id = await reader.read(2)
        writer.write("OK".encode())
        await writer.drain()
        writer.close()
