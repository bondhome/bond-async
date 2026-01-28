"""Unit tests for DeviceType."""

from bond_async.device_type import DeviceType


def test_compare_device_types():
    """Tests that constants are configured and compared correctly."""
    assert DeviceType.CEILING_FAN == "CF"
    assert DeviceType.is_fan("CF")

    assert DeviceType.MOTORIZED_SHADES == "MS"
    assert DeviceType.is_shades("MS")

    assert DeviceType.FIREPLACE == "FP"
    assert DeviceType.is_fireplace("FP")

    assert DeviceType.GENERIC_DEVICE == "GX"
    assert DeviceType.is_generic("GX")

    assert DeviceType.AIR_CONDITIONER == "AC"
    assert DeviceType.is_air_conditioner("AC")

    assert DeviceType.GARAGE_DOOR == "GD"
    assert DeviceType.is_garage_door("GD")

    assert DeviceType.BIDET == "BD"
    assert DeviceType.is_bidet("BD")

    assert DeviceType.LIGHT == "LT"
    assert DeviceType.is_light("LT")

    assert DeviceType.SWITCH == "SW"
    assert DeviceType.is_switch("SW")

    assert DeviceType.HEATER == "HT"
    assert DeviceType.is_heater("HT")
