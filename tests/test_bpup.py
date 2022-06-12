"""Unit tests for Bond BPUP."""

from unittest.mock import call, MagicMock, patch
from typing import Optional
import asyncio
import pytest
import datetime as dt

from . import mock_time_changed
from bond_async.bpup import BPUPSubscriptions, BPUProtocol, start_bpup

MOCK_ADDR = ("127.0.0.1", 1)


def mock_protocol_connection_lost(
    protocol: asyncio.BaseProtocol, exc: Optional[Exception]
) -> None:
    """Mock an asyncio.Protocol connection lost callback."""
    protocol.connection_lost(exc)
    protocol.transport.is_closing = MagicMock(return_value=True)


@pytest.fixture(name="transport")
def transport_fixture():
    """Creates transport fixture."""
    transport = MagicMock(auto_spec=asyncio.DatagramTransport)
    transport.is_closing = MagicMock(return_value=False)

    def _mock_close(*_):
        transport.is_closing = MagicMock(return_value=True)

    transport.close = _mock_close
    return transport


@pytest.mark.asyncio
async def test_protocol_keep_alive_close(transport):
    bpup_subscriptions = BPUPSubscriptions()
    loop = asyncio.get_event_loop()
    bpup_protocol = BPUProtocol(bpup_subscriptions)

    bpup_protocol.connection_made(transport)
    assert transport.sendto.mock_calls == [call(b"\n")]
    transport.sendto.reset_mock()

    mock_time_changed(loop, dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=60))
    assert transport.sendto.mock_calls == [call(b"\n")]
    transport.sendto.reset_mock()

    bpup_protocol.stop()

    mock_time_changed(
        loop, dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=120)
    )
    assert transport.sendto.mock_calls == []


@pytest.mark.asyncio
async def test_protocol_keep_connection_lost_no_error(transport, caplog):
    bpup_subscriptions = BPUPSubscriptions()
    loop = asyncio.get_event_loop()
    bpup_protocol = BPUProtocol(bpup_subscriptions)

    bpup_protocol.connection_made(transport)
    assert transport.sendto.mock_calls == [call(b"\n")]
    transport.sendto.reset_mock()
    assert bpup_subscriptions.alive is False
    bpup_protocol.datagram_received(
        b'{"B":"KNKSADE42149","d":0,"v":"v2.29.2-beta"}\n', MOCK_ADDR
    )
    assert bpup_subscriptions.alive is True

    mock_time_changed(loop, dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=60))
    assert transport.sendto.mock_calls == [call(b"\n")]
    transport.sendto.reset_mock()

    mock_protocol_connection_lost(bpup_protocol, None)
    assert "BPUP connection lost" not in caplog.text
    assert bpup_subscriptions.alive is False

    mock_time_changed(
        loop, dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=120)
    )
    assert transport.sendto.mock_calls == []


@pytest.mark.asyncio
async def test_protocol_keep_connection_lost_with_error(transport, caplog):
    bpup_subscriptions = BPUPSubscriptions()
    loop = asyncio.get_event_loop()
    bpup_protocol = BPUProtocol(bpup_subscriptions)

    bpup_protocol.connection_made(transport)
    assert transport.sendto.mock_calls == [call(b"\n")]
    transport.sendto.reset_mock()
    assert bpup_subscriptions.alive is False
    bpup_protocol.datagram_received(
        b'{"B":"KNKSADE42149","d":0,"v":"v2.29.2-beta"}\n', MOCK_ADDR
    )

    mock_time_changed(loop, dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=60))
    assert transport.sendto.mock_calls == [call(b"\n")]
    transport.sendto.reset_mock()
    assert bpup_subscriptions.alive is True

    mock_protocol_connection_lost(bpup_protocol, OSError())

    assert "BPUP connection lost" in caplog.text
    assert bpup_subscriptions.alive is False

    assert transport.sendto.mock_calls == []
    mock_time_changed(
        loop, dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=120)
    )
    assert transport.sendto.mock_calls == []


@pytest.mark.asyncio
async def test_protocol_subscriptions(transport, caplog):
    bpup_subscriptions = BPUPSubscriptions()
    bpup_protocol = BPUProtocol(bpup_subscriptions)
    last_msg = None

    def _on_new_message(msg):
        nonlocal last_msg
        last_msg = msg

    bpup_subscriptions.subscribe("1", _on_new_message)

    bpup_protocol.connection_made(transport)
    # Make sure we can do it again
    bpup_protocol.connection_made(transport)
    bpup_protocol.datagram_received(
        b'{"B":"KNKSADE42149","d":0,"v":"v2.29.2-beta"}\n', MOCK_ADDR
    )

    bpup_protocol.datagram_received(
        b'{"t":"devices/1/state","s":200,"b":{"power":1,"speed":1,"timer":0,"breeze":[0,50,50],"_":"690b6aff"}}\n',
        MOCK_ADDR,
    )

    assert last_msg == {
        "t": "devices/1/state",
        "s": 200,
        "b": {
            "power": 1,
            "speed": 1,
            "timer": 0,
            "breeze": [0, 50, 50],
            "_": "690b6aff",
        },
    }

    bpup_protocol.datagram_received(
        b'{"t":"devices/1/state","s":200,"b":{"power":1,"speed":1,"timer":0,"breeze":[0,50,50],"_":"690b6aff"}}\n',
        MOCK_ADDR,
    )
    # 500 error should not trigger a new message
    assert last_msg == {
        "t": "devices/1/state",
        "s": 200,
        "b": {
            "power": 1,
            "speed": 1,
            "timer": 0,
            "breeze": [0, 50, 50],
            "_": "690b6aff",
        },
    }

    last_msg = {}
    bpup_subscriptions.unsubscribe("1", _on_new_message)
    bpup_protocol.datagram_received(
        b'{"t":"devices/1/state","s":200,"b":{"power":1,"speed":1,"timer":0,"breeze":[0,50,50],"_":"690b6aff"}}\n',
        MOCK_ADDR,
    )
    assert last_msg == {}

    bpup_protocol.datagram_received(
        b'{"B":"KVPRBDGXXXXX","_error_id":633,"_error_msg":"BPUP client timeout"}',
        MOCK_ADDR,
    )
    assert last_msg == {}

    bpup_protocol.datagram_received(
        b"GIGO",
        MOCK_ADDR,
    )
    assert "Failed to process BPUP message" in caplog.text
    assert "GIGO" in caplog.text


@pytest.mark.asyncio
async def test_protocol_errors(transport, caplog):
    bpup_subscriptions = BPUPSubscriptions()
    bpup_protocol = BPUProtocol(bpup_subscriptions)
    bpup_protocol.connection_made(transport)
    bpup_protocol.error_received(OSError())
    assert "BPUP error" in caplog.text


@pytest.mark.asyncio
async def test_start_bpup(transport):
    loop = asyncio.get_event_loop()
    bpup_subscriptions = BPUPSubscriptions()

    async def _mock_create_datagram_endpoint(func, remote_addr=None):
        return transport, func()

    with patch.object(loop, "create_datagram_endpoint", _mock_create_datagram_endpoint):
        stop = await start_bpup("127.0.0.1", bpup_subscriptions)

    stop()
