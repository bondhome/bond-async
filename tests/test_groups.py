"""Unit tests for Bond API wrapper."""

import pytest
from aiohttp import ClientSession, ClientTimeout
from aioresponses import CallbackResult, aioresponses

from bond_async import Action, Bond, Direction


@pytest.fixture(name="bond")
def bond_fixture():
    """Creates Bond fixture."""
    return Bond("test-host", "test-token")


@pytest.mark.asyncio
async def test_groups_supported(bond: Bond):
    """Tests checking if Bond supports groups."""
    with aioresponses() as response:
        response.get(
            "http://test-host/v2/",
            payload={
                "_": "b7e976b1",
                "__": "00000000",
                "devices": {"_": "0b64ba79"},
                "signal": {"_": "00000000"},
                "groups": {"_": "71ce683b"},
                "sys": {"_": "89858d62"},
                "api": {"_": "d00c7b8f"},
                "bridge": {"_": "df239de9"},
                "token": {"_": "aa72441a"},
            },
        )
        actual = await bond.supports_groups()
        assert actual == True


@pytest.mark.asyncio
async def test_groups_unsupported(bond: Bond):
    """Tests checking if Bond supports groups."""
    with aioresponses() as response:
        response.get(
            "http://test-host/v2/",
            payload={
                "_": "b7e976b1",
                "__": "00000000",
                "devices": {"_": "0b64ba79"},
                "signal": {"_": "00000000"},
                "sys": {"_": "89858d62"},
                "api": {"_": "d00c7b8f"},
                "bridge": {"_": "df239de9"},
                "token": {"_": "aa72441a"},
            },
        )
        actual = await bond.supports_groups()
        assert actual == False


@pytest.mark.asyncio
async def test_groups(bond: Bond):
    """Tests API to get a list of group IDs."""
    with aioresponses() as response:
        response.get(
            "http://test-host/v2/groups",
            payload={
                "_": "some-hash",
                "__": "some-other-hash",
                "group-1": {"_": "some-hash"},
                "group-2": {"_": "some-hash"},
            },
        )
        actual = await bond.groups()
        assert actual == ["group-1", "group-2"]


@pytest.mark.asyncio
async def test_group(bond: Bond):
    """Tests API to get group details."""
    with aioresponses() as response:
        response.get(
            "http://test-host/v2/groups/group-1", payload={"some": "group details"}
        )
        actual = await bond.group("group-1")
        assert actual == {"some": "group details"}


@pytest.mark.asyncio
async def test_group_properties(bond: Bond):
    """Tests API to get group properties."""
    with aioresponses() as response:
        response.get(
            "http://test-host/v2/groups/group-1/properties",
            payload={"some": "group properties"},
        )
        actual = await bond.group_properties("group-1")
        assert actual == {"some": "group properties"}


@pytest.mark.asyncio
async def test_group_state(bond: Bond):
    """Tests API to get group state."""
    with aioresponses() as response:
        response.get(
            "http://test-host/v2/groups/group-1/state",
            payload={"some": "group state"},
        )
        actual = await bond.group_state("group-1")
        assert actual == {"some": "group state"}


@pytest.mark.asyncio
async def test_turn_on(bond: Bond):
    """Tests turn_on action delegates to API."""
    with aioresponses() as response:

        def callback(_url, **kwargs):
            assert kwargs.get("json") == {}
            return CallbackResult()

        response.put(
            "http://test-host/v2/groups/test-group-id/actions/TurnOn",
            callback=callback,
        )
        await bond.group_action("test-group-id", Action.turn_on())


@pytest.mark.asyncio
async def test_turn_off(bond: Bond):
    """Tests turn_off action delegates to API."""
    with aioresponses() as response:

        def callback(_url, **kwargs):
            assert kwargs.get("json") == {}
            return CallbackResult()

        response.put(
            "http://test-host/v2/groups/test-group-id/actions/TurnOff",
            callback=callback,
        )
        await bond.group_action("test-group-id", Action.turn_off())


@pytest.mark.asyncio
async def test_open(bond: Bond):
    """Tests open action delegates to API."""
    with aioresponses() as response:

        def callback(_url, **kwargs):
            assert kwargs.get("json") == {}
            return CallbackResult()

        response.put(
            "http://test-host/v2/groups/test-group-id/actions/Open", callback=callback
        )
        await bond.group_action("test-group-id", Action.open())


@pytest.mark.asyncio
async def test_tilt_open(bond: Bond):
    """Tests tilt open action delegates to API."""
    with aioresponses() as response:

        def callback(_url, **kwargs):
            assert kwargs.get("json") == {}
            return CallbackResult()

        response.put(
            "http://test-host/v2/groups/test-group-id/actions/TiltOpen",
            callback=callback,
        )
        await bond.group_action("test-group-id", Action.tilt_open())


@pytest.mark.asyncio
async def test_close(bond: Bond):
    """Tests close action delegates to API."""
    with aioresponses() as response:

        def callback(_url, **kwargs):
            assert kwargs.get("json") == {}
            return CallbackResult()

        response.put(
            "http://test-host/v2/groups/test-group-id/actions/Close",
            callback=callback,
        )
        await bond.group_action("test-group-id", Action.close())


@pytest.mark.asyncio
async def test_tilt_close(bond: Bond):
    """Tests tilt close action delegates to API."""
    with aioresponses() as response:

        def callback(_url, **kwargs):
            assert kwargs.get("json") == {}
            return CallbackResult()

        response.put(
            "http://test-host/v2/groups/test-group-id/actions/TiltClose",
            callback=callback,
        )
        await bond.group_action("test-group-id", Action.tilt_close())


@pytest.mark.asyncio
async def test_hold(bond: Bond):
    """Tests hold action delegates to API."""
    with aioresponses() as response:

        def callback(_url, **kwargs):
            assert kwargs.get("json") == {}
            return CallbackResult()

        response.put(
            "http://test-host/v2/groups/test-group-id/actions/Hold", callback=callback
        )
        await bond.group_action("test-group-id", Action.hold())


@pytest.mark.asyncio
async def test_set_speed(bond: Bond):
    """Tests set_speed action delegates to API."""
    with aioresponses() as response:

        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"argument": 2}
            return CallbackResult()

        response.put(
            "http://test-host/v2/groups/test-group-id/actions/SetSpeed",
            callback=callback,
        )
        await bond.group_action("test-group-id", Action.set_speed(2))


@pytest.mark.asyncio
async def test_set_speed_belief(bond: Bond):
    """Tests set_speed_belief action delegates to API."""
    with aioresponses() as response:

        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"speed": 2}
            return CallbackResult()

        response.patch(
            "http://test-host/v2/groups/test-group-id/state", callback=callback
        )
        await bond.group_action("test-group-id", Action.set_speed_belief(2))


@pytest.mark.asyncio
async def test_set_brightness_belief(bond: Bond):
    """Tests set_brightness_belief action delegates to API."""
    with aioresponses() as response:

        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"brightness": 2}
            return CallbackResult()

        response.patch(
            "http://test-host/v2/groups/test-group-id/state", callback=callback
        )
        await bond.group_action("test-group-id", Action.set_brightness_belief(2))


@pytest.mark.asyncio
async def test_set_power_state_belief(bond: Bond):
    """Tests set_power_state_belief action delegates to API."""
    with aioresponses() as response:

        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"power": 1}
            return CallbackResult()

        response.patch(
            "http://test-host/v2/groups/test-group-id/state", callback=callback
        )
        await bond.group_action("test-group-id", Action.set_power_state_belief(True))


@pytest.mark.asyncio
async def test_set_light_state_belief(bond: Bond):
    """Tests set_light_state_belief action delegates to API."""
    with aioresponses() as response:

        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"light": 0}
            return CallbackResult()

        response.patch(
            "http://test-host/v2/groups/test-group-id/state", callback=callback
        )
        await bond.group_action("test-group-id", Action.set_light_state_belief(False))


@pytest.mark.asyncio
async def test_turn_light_on(bond: Bond):
    """Tests turn_light_on action delegates to API."""
    with aioresponses() as response:

        def callback(_url, **kwargs):
            assert kwargs.get("json") == {}
            return CallbackResult()

        response.put(
            "http://test-host/v2/groups/test-group-id/actions/TurnLightOn",
            callback=callback,
        )
        await bond.group_action("test-group-id", Action.turn_light_on())


@pytest.mark.asyncio
async def test_turn_light_off(bond: Bond):
    """Tests turn_light_off action delegates to API."""
    with aioresponses() as response:

        def callback(_url, **kwargs):
            assert kwargs.get("json") == {}
            return CallbackResult()

        response.put(
            "http://test-host/v2/groups/test-group-id/actions/TurnLightOff",
            callback=callback,
        )
        await bond.group_action("test-group-id", Action.turn_light_off())


@pytest.mark.asyncio
async def test_set_brightness(bond: Bond):
    """Tests set_brightness action delegates to API."""
    with aioresponses() as response:

        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"argument": 50}
            return CallbackResult()

        response.put(
            "http://test-host/v2/groups/test-group-id/actions/SetBrightness",
            callback=callback,
        )
        await bond.group_action("test-group-id", Action.set_brightness(50))


@pytest.mark.asyncio
async def test_set_color_temperature(bond: Bond):
    """Tests set_color_temperature action delegates to API."""
    with aioresponses() as response:

        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"argument": 3000}
            return CallbackResult()

        response.put(
            "http://test-host/v2/groups/test-group-id/actions/SetColorTemp",
            callback=callback,
        )
        await bond.group_action("test-group-id", Action.set_color_temperature(3000))


@pytest.mark.asyncio
async def test_increase_color_temperature(bond: Bond):
    """Tests increase_color_temperature action delegates to API."""
    with aioresponses() as response:

        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"argument": 100}
            return CallbackResult()

        response.put(
            "http://test-host/v2/groups/test-group-id/actions/IncreaseColorTemp",
            callback=callback,
        )
        await bond.group_action("test-group-id", Action.increase_color_temperature(100))


@pytest.mark.asyncio
async def test_decrease_color_temperature(bond: Bond):
    """Tests decrease_color_temperature action delegates to API."""
    with aioresponses() as response:

        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"argument": 100}
            return CallbackResult()

        response.put(
            "http://test-host/v2/groups/test-group-id/actions/DecreaseColorTemp",
            callback=callback,
        )
        await bond.group_action("test-group-id", Action.decrease_color_temperature(100))


@pytest.mark.asyncio
async def test_set_direction_forward(bond: Bond):
    """Tests set_direction action delegates to API with correct value for forward."""
    with aioresponses() as response:

        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"argument": 1}
            return CallbackResult()

        response.put(
            "http://test-host/v2/groups/test-group-id/actions/SetDirection",
            callback=callback,
        )
        await bond.group_action(
            "test-group-id", Action.set_direction(Direction.FORWARD)
        )


@pytest.mark.asyncio
async def test_set_direction_reverse(bond: Bond):
    """Tests set_direction action delegates to API with correct value for reverse."""
    with aioresponses() as response:

        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"argument": -1}
            return CallbackResult()

        response.put(
            "http://test-host/v2/groups/test-group-id/actions/SetDirection",
            callback=callback,
        )
        await bond.group_action(
            "test-group-id", Action.set_direction(Direction.REVERSE)
        )


@pytest.mark.asyncio
async def test_set_flame(bond: Bond):
    """Tests set_flame action delegates to API."""
    with aioresponses() as response:

        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"argument": 50}
            return CallbackResult()

        response.put(
            "http://test-host/v2/groups/test-group-id/actions/SetFlame",
            callback=callback,
        )
        await bond.group_action("test-group-id", Action.set_flame(50))


@pytest.mark.asyncio
async def test_set_position(bond: Bond):
    """Tests set_position action delegates to API."""
    with aioresponses() as response:

        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"argument": 50}
            return CallbackResult()

        response.put(
            "http://test-host/v2/groups/test-group-id/actions/SetPosition",
            callback=callback,
        )
        await bond.group_action("test-group-id", Action.set_position(50))


@pytest.mark.asyncio
async def test_increase_position(bond: Bond):
    """Tests increase_position action delegates to API."""
    with aioresponses() as response:

        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"argument": 50}
            return CallbackResult()

        response.put(
            "http://test-host/v2/groups/test-group-id/actions/IncreasePosition",
            callback=callback,
        )
        await bond.group_action("test-group-id", Action.increase_position(50))


@pytest.mark.asyncio
async def test_decrease_position(bond: Bond):
    """Tests decrease_position action delegates to API."""
    with aioresponses() as response:

        def callback(_url, **kwargs):
            assert kwargs.get("json") == {"argument": 50}
            return CallbackResult()

        response.put(
            "http://test-host/v2/groups/test-group-id/actions/DecreasePosition",
            callback=callback,
        )
        await bond.group_action("test-group-id", Action.decrease_position(50))
