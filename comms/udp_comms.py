"""
A lightweight UDP-based communications emulator that can be run locally. It supports simple broadcast by sending to sequential ports on localhost.
This is not for real networking use — it's a testbed for local simulation.
"""
import asyncio
import json
import socket
from typing import AsyncGenerator, Tuple, Any


class UDPComms:
    def __init__(self, host: str, port: int, port_range: int = 64):
        self.host = host
        self.port = port
        self.port_range = port_range
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # bind to port so we can receive
        self.sock.bind((host, port))
        self.loop = asyncio.get_event_loop()
        self.closed = False

    async def broadcast(self, message: dict):
        # naive: send the serialized packet to the next port_range ports
        data = json.dumps(message).encode('utf-8')
        for p in range(self.port - (self.port % self.port_range), self.port - (self.port % self.port_range) + self.port_range):
            # skip sending to self port if you like, but keep it simple
            self.sock.sendto(data, (self.host, p))

    async def receive_loop(self) -> AsyncGenerator[Tuple[int, dict], None]:
        # wrap blocking socket in executor to get data
        while not self.closed:
            data, addr = await self.loop.run_in_executor(None, self.sock.recvfrom, 65536)
            try:
                payload = json.loads(data.decode('utf-8'))
            except Exception:
                continue
            yield addr[1], payload

    def close(self):
        self.closed = True
        try:
            self.sock.close()
        except Exception:
            pass
