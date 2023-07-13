"""Bond BPUP wrapper."""

import asyncio
import logging
import time
from typing import Any, Callable, Dict, List, Optional, cast

import orjson

BPUP_INIT_PUSH_MESSAGE = b"\n"
BPUP_PORT = 30007
BPUP_ALIVE_TIMEOUT = 70

_LOGGER = logging.getLogger(__name__)


class BPUPSubscriptions:
    """Store BPUP subscriptions."""

    def __init__(self) -> None:
        """Init and store callbacks."""
        self._callbacks: Dict[str, List[Callable]] = {}
        self.last_message_time: float = -BPUP_ALIVE_TIMEOUT

    @property
    def alive(self) -> bool:
        """Return if the subscriptions are considered alive."""
        return (time.monotonic() - self.last_message_time) < BPUP_ALIVE_TIMEOUT

    def connection_lost(self) -> None:
        """Set the last message time to never."""
        self.last_message_time = -BPUP_ALIVE_TIMEOUT

    def subscribe(self, device_id: str, callback: Callable) -> None:
        """Subscribe to BPUP updates."""
        self._callbacks.setdefault(device_id, []).append(callback)

    def unsubscribe(self, device_id: str, callback: Callable) -> None:
        """Unsubscribe from BPUP updates."""
        self._callbacks[device_id].remove(callback)

    def notify(self, json_msg: Dict[str, Any]) -> None:
        """Notify subscribers of an update."""
        self.last_message_time = time.monotonic()

        if json_msg.get("s") != 200:
            return

        topic = json_msg["t"].split("/")
        device_id = topic[1]

        for callback in self._callbacks.get(device_id, []):
            callback(json_msg)


class BPUProtocol(asyncio.Protocol):
    """Implements BPU Protocol."""

    def __init__(self, bpup_subscriptions: BPUPSubscriptions) -> None:
        """Create BPU Protocol."""
        self.loop = asyncio.get_event_loop()
        self.bpup_subscriptions: BPUPSubscriptions = bpup_subscriptions
        self.transport: Optional[asyncio.DatagramTransport] = None
        self.keep_alive: Optional[asyncio.TimerHandle] = None

    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        """Connect or reconnect to the device."""
        self.transport = cast(asyncio.DatagramTransport, transport)
        if self.keep_alive:
            self.keep_alive.cancel()
            self.keep_alive = None
        self.send_keep_alive()

    def send_keep_alive(self) -> None:
        """Send a keep alive every 60 seconds per the protocol."""
        if not self.transport or self.transport.is_closing():
            return
        self.transport.sendto(BPUP_INIT_PUSH_MESSAGE)
        self.keep_alive = self.loop.call_later(60, self.send_keep_alive)

    def datagram_received(self, data: bytes, addr: Any) -> None:
        """Process incoming state changes."""
        _LOGGER.debug("%s: BPUP message: %s", addr, data)
        try:
            self.bpup_subscriptions.notify(orjson.loads(data.decode().rstrip("\n")))
        except orjson.JSONDecodeError as ex:
            _LOGGER.warning(
                "%s: Failed to process BPUP message: %s: %s", addr, data, ex
            )

    def error_received(self, exc: Optional[Exception]) -> None:
        """Log errors."""
        assert self.transport is not None
        _LOGGER.error(
            "BPUP error (peer:%s sock:%s): %s",
            self.transport.get_extra_info("peername"),
            self.transport.get_extra_info("sockname"),
            exc,
        )

    def connection_lost(self, exc: Optional[Exception]) -> None:
        """Log connection lost."""
        assert self.transport is not None
        self.bpup_subscriptions.connection_lost()
        if exc:
            _LOGGER.error(
                "BPUP connection lost (peer:%s sock:%s): %s",
                self.transport.get_extra_info("peername"),
                self.transport.get_extra_info("sockname"),
                exc,
            )

    def stop(self) -> None:
        """Stop the client."""
        _LOGGER.debug("BPUP connection stopping: %s", self.transport)
        self.bpup_subscriptions.connection_lost()
        if self.transport:
            self.transport.close()


async def start_bpup(
    host_ip_addr: str, bpup_subscriptions: BPUPSubscriptions
) -> Callable:
    """Create the socket and protocol."""
    loop = asyncio.get_event_loop()

    _, protocol = await loop.create_datagram_endpoint(
        lambda: BPUProtocol(bpup_subscriptions),
        remote_addr=(host_ip_addr, BPUP_PORT),
    )
    bpup_protocol = cast(BPUProtocol, protocol)
    return bpup_protocol.stop
