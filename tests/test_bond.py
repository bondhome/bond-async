"""Unit tests for Bond API wrapper."""

import pytest
from aiohttp import ClientSession, ClientTimeout
from aioresponses import CallbackResult, aioresponses

from bond_async import Action, Bond, Direction, RequestorUUID
from bond_async.bond_type import BondType


@pytest.fixture(name="bond")
def bond_fixture():
    """Creates Bond fixture."""
    return Bond("test-host", "test-token")


@pytest.mark.asyncio
async def test_optional_overrides():
    """Tests using external session."""
    async with ClientSession() as session:
        timeout: ClientTimeout = ClientTimeout(total=1)
        bond: Bond = Bond("test-host", "test-token", session=session, timeout=timeout)
        with aioresponses() as response:
            response.get("http://test-host/v2/sys/version", payload={"some": "version"})
            actual = await bond.version()
            assert actual == {"some": "version"}


@pytest.mark.asyncio
async def test_illegal_requestor_uuid():
    """Tests using illegal requestor UUID."""
    with pytest.raises(ValueError):
        Bond("test-host", "test-token", requestor_uuid=RequestorUUID.TEST)


@pytest.mark.asyncio
async def test_legal_requestor_uuid():
    """Tests using legal requestor UUID."""
    bond = Bond("test-host", "test-token", requestor_uuid=RequestorUUID.ANONYMOUS)
    assert bond._requestor_uuid == RequestorUUID.ANONYMOUS


@pytest.mark.asyncio
async def test_create_message_id():
    bond = Bond("test-host", "test-token", requestor_uuid=RequestorUUID.ANONYMOUS)
    message_id = bond._Bond__create_message_id()
    session_id = bond._session_uuid
    assert message_id[:2] == "ff"
    assert message_id[2:6] == session_id
    assert len(message_id) == 16

    # a new call should generate a new message id, but the requestor uuid and session id should be the same
    new_message_id = bond._Bond__create_message_id()
    assert new_message_id[:2] == "ff"
    assert new_message_id[2:6] == session_id
    assert len(new_message_id) == 16
    assert new_message_id != message_id


@pytest.mark.asyncio
async def test_msg_id_in_request_header(bond: Bond):
    """Tests that the message id is in the request header."""
    with aioresponses() as response:
        response.get(
            "http://test-host/v2/sys/version",
            payload={"some": "version"},
        )
        await bond.version()
        headers = next(iter(response.requests.values()))[0].kwargs["headers"]
        assert "BOND-UUID" in headers
        msg_id = headers["BOND-UUID"]
        assert msg_id[:2] == "ff"
        assert msg_id[2:6] == bond._session_uuid
        assert len(msg_id) == 16


@pytest.mark.asyncio
async def test_version(bond: Bond):
    """Tests version API."""
    with aioresponses() as response:
        response.get("http://test-host/v2/sys/version", payload={"some": "version"})
        actual = await bond.version()
        assert actual == {"some": "version"}


@pytest.mark.asyncio
async def test_bond_type(bond: Bond):
    """Tests version API."""
    with aioresponses() as response:
        response.get(
            "http://test-host/v2/sys/version", payload={"bondid": "KSMJWCE12345"}
        )
        actual = await bond.bond_type()
        assert actual == BondType.SBB_CEILING_FAN


@pytest.mark.asyncio
async def test_bridge(bond: Bond):
    """Tests bridge API."""
    with aioresponses() as response:
        response.get(
            "http://test-host/v2/bridge",
            payload={"name": "name", "location": "location"},
        )
        actual = await bond.bridge()
        assert actual == {"name": "name", "location": "location"}


@pytest.mark.asyncio
async def test_token(bond: Bond):
    """Tests token API."""
    with aioresponses() as response:
        response.get(
            "http://test-host/v2/token",
            payload={"locked": 0, "token": "8f514567acaf9869"},
        )
        actual = await bond.token()
        assert actual == {"locked": 0, "token": "8f514567acaf9869"}


@pytest.mark.asyncio
async def test_devices(bond: Bond):
    """Tests API to get a list of device IDs."""
    with aioresponses() as response:
        response.get(
            "http://test-host/v2/devices",
            payload={
                "_": "some-hash",
                "__": "some-other-hash",
                "device-1": {"_": "some-hash"},
                "device-2": {"_": "some-hash"},
            },
        )
        actual = await bond.devices()
        assert actual == ["device-1", "device-2"]


@pytest.mark.asyncio
async def test_device(bond: Bond):
    """Tests API to get device details."""
    with aioresponses() as response:
        response.get(
            "http://test-host/v2/devices/device-1", payload={"some": "device details"}
        )
        actual = await bond.device("device-1")
        assert actual == {"some": "device details"}


@pytest.mark.asyncio
async def test_device_properties(bond: Bond):
    """Tests API to get device properties."""
    with aioresponses() as response:
        response.get(
            "http://test-host/v2/devices/device-1/properties",
            payload={"some": "device properties"},
        )
        actual = await bond.device_properties("device-1")
        assert actual == {"some": "device properties"}


@pytest.mark.asyncio
async def test_device_state(bond: Bond):
    """Tests API to get device state."""
    with aioresponses() as response:
        response.get(
            "http://test-host/v2/devices/device-1/state",
            payload={"some": "device state"},
        )
        actual = await bond.device_state("device-1")
        assert actual == {"some": "device state"}


@pytest.mark.asyncio
async def test_turn_on(bond: Bond):
    """Tests turn_on action delegates to API."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {}
            return CallbackResult()

        response.put(
            "http://test-host/v2/devices/test-device-id/actions/TurnOn",
            callback=callback,
        )
        await bond.action("test-device-id", Action.turn_on())


@pytest.mark.asyncio
async def test_turn_off(bond: Bond):
    """Tests turn_off action delegates to API."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {}
            return CallbackResult()

        response.put(
            "http://test-host/v2/devices/test-device-id/actions/TurnOff",
            callback=callback,
        )
        await bond.action("test-device-id", Action.turn_off())


@pytest.mark.asyncio
async def test_open(bond: Bond):
    """Tests open action delegates to API."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {}
            return CallbackResult()

        response.put(
            "http://test-host/v2/devices/test-device-id/actions/Open", callback=callback
        )
        await bond.action("test-device-id", Action.open())


@pytest.mark.asyncio
async def test_tilt_open(bond: Bond):
    """Tests tilt open action delegates to API."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {}
            return CallbackResult()

        response.put(
            "http://test-host/v2/devices/test-device-id/actions/TiltOpen",
            callback=callback,
        )
        await bond.action("test-device-id", Action.tilt_open())


@pytest.mark.asyncio
async def test_close(bond: Bond):
    """Tests close action delegates to API."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {}
            return CallbackResult()

        response.put(
            "http://test-host/v2/devices/test-device-id/actions/Close",
            callback=callback,
        )
        await bond.action("test-device-id", Action.close())


@pytest.mark.asyncio
async def test_tilt_close(bond: Bond):
    """Tests tilt close action delegates to API."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {}
            return CallbackResult()

        response.put(
            "http://test-host/v2/devices/test-device-id/actions/TiltClose",
            callback=callback,
        )
        await bond.action("test-device-id", Action.tilt_close())


@pytest.mark.asyncio
async def test_hold(bond: Bond):
    """Tests hold action delegates to API."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {}
            return CallbackResult()

        response.put(
            "http://test-host/v2/devices/test-device-id/actions/Hold", callback=callback
        )
        await bond.action("test-device-id", Action.hold())


@pytest.mark.asyncio
async def test_set_speed(bond: Bond):
    """Tests set_speed action delegates to API."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"argument": 2}
            return CallbackResult()

        response.put(
            "http://test-host/v2/devices/test-device-id/actions/SetSpeed",
            callback=callback,
        )
        await bond.action("test-device-id", Action.set_speed(2))


@pytest.mark.asyncio
async def test_set_speed_belief(bond: Bond):
    """Tests set_speed_belief action delegates to API."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"speed": 2}
            return CallbackResult()

        response.patch(
            "http://test-host/v2/devices/test-device-id/state", callback=callback
        )
        await bond.action("test-device-id", Action.set_speed_belief(2))


@pytest.mark.asyncio
async def test_set_brightness_belief(bond: Bond):
    """Tests set_brightness_belief action delegates to API."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"brightness": 2}
            return CallbackResult()

        response.patch(
            "http://test-host/v2/devices/test-device-id/state", callback=callback
        )
        await bond.action("test-device-id", Action.set_brightness_belief(2))


@pytest.mark.asyncio
async def test_set_power_state_belief(bond: Bond):
    """Tests set_power_state_belief action delegates to API."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"power": 1}
            return CallbackResult()

        response.patch(
            "http://test-host/v2/devices/test-device-id/state", callback=callback
        )
        await bond.action("test-device-id", Action.set_power_state_belief(True))


@pytest.mark.asyncio
async def test_set_light_state_belief(bond: Bond):
    """Tests set_light_state_belief action delegates to API."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"light": 0}
            return CallbackResult()

        response.patch(
            "http://test-host/v2/devices/test-device-id/state", callback=callback
        )
        await bond.action("test-device-id", Action.set_light_state_belief(False))


@pytest.mark.asyncio
async def test_turn_light_on(bond: Bond):
    """Tests turn_light_on action delegates to API."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {}
            return CallbackResult()

        response.put(
            "http://test-host/v2/devices/test-device-id/actions/TurnLightOn",
            callback=callback,
        )
        await bond.action("test-device-id", Action.turn_light_on())


@pytest.mark.asyncio
async def test_turn_light_off(bond: Bond):
    """Tests turn_light_off action delegates to API."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {}
            return CallbackResult()

        response.put(
            "http://test-host/v2/devices/test-device-id/actions/TurnLightOff",
            callback=callback,
        )
        await bond.action("test-device-id", Action.turn_light_off())


@pytest.mark.asyncio
async def test_set_brightness(bond: Bond):
    """Tests set_brightness action delegates to API."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"argument": 50}
            return CallbackResult()

        response.put(
            "http://test-host/v2/devices/test-device-id/actions/SetBrightness",
            callback=callback,
        )
        await bond.action("test-device-id", Action.set_brightness(50))


@pytest.mark.asyncio
async def test_set_color_temperature(bond: Bond):
    """Tests set_color_temperature action delegates to API."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"argument": 3000}
            return CallbackResult()

        response.put(
            "http://test-host/v2/devices/test-device-id/actions/SetColorTemp",
            callback=callback,
        )
        await bond.action("test-device-id", Action.set_color_temperature(3000))


@pytest.mark.asyncio
async def test_increase_color_temperature(bond: Bond):
    """Tests increase_color_temperature action delegates to API."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"argument": 100}
            return CallbackResult()

        response.put(
            "http://test-host/v2/devices/test-device-id/actions/IncreaseColorTemp",
            callback=callback,
        )
        await bond.action("test-device-id", Action.increase_color_temperature(100))


@pytest.mark.asyncio
async def test_decrease_color_temperature(bond: Bond):
    """Tests decrease_color_temperature action delegates to API."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"argument": 100}
            return CallbackResult()

        response.put(
            "http://test-host/v2/devices/test-device-id/actions/DecreaseColorTemp",
            callback=callback,
        )
        await bond.action("test-device-id", Action.decrease_color_temperature(100))


@pytest.mark.asyncio
async def test_set_direction_forward(bond: Bond):
    """Tests set_direction action delegates to API with correct value for forward."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"argument": 1}
            return CallbackResult()

        response.put(
            "http://test-host/v2/devices/test-device-id/actions/SetDirection",
            callback=callback,
        )
        await bond.action("test-device-id", Action.set_direction(Direction.FORWARD))


@pytest.mark.asyncio
async def test_set_direction_reverse(bond: Bond):
    """Tests set_direction action delegates to API with correct value for reverse."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"argument": -1}
            return CallbackResult()

        response.put(
            "http://test-host/v2/devices/test-device-id/actions/SetDirection",
            callback=callback,
        )
        await bond.action("test-device-id", Action.set_direction(Direction.REVERSE))


@pytest.mark.asyncio
async def test_set_flame(bond: Bond):
    """Tests set_flame action delegates to API."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"argument": 50}
            return CallbackResult()

        response.put(
            "http://test-host/v2/devices/test-device-id/actions/SetFlame",
            callback=callback,
        )
        await bond.action("test-device-id", Action.set_flame(50))


@pytest.mark.asyncio
async def test_set_position(bond: Bond):
    """Tests set_position action delegates to API."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"argument": 50}
            return CallbackResult()

        response.put(
            "http://test-host/v2/devices/test-device-id/actions/SetPosition",
            callback=callback,
        )
        await bond.action("test-device-id", Action.set_position(50))


@pytest.mark.asyncio
async def test_increase_position(bond: Bond):
    """Tests increase_position action delegates to API."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"argument": 50}
            return CallbackResult()

        response.put(
            "http://test-host/v2/devices/test-device-id/actions/IncreasePosition",
            callback=callback,
        )
        await bond.action("test-device-id", Action.increase_position(50))


@pytest.mark.asyncio
async def test_decrease_position(bond: Bond):
    """Tests decrease_position action delegates to API."""
    with aioresponses() as response:
        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"argument": 50}
            return CallbackResult()

        response.put(
            "http://test-host/v2/devices/test-device-id/actions/DecreasePosition",
            callback=callback,
        )
        await bond.action("test-device-id", Action.decrease_position(50))
