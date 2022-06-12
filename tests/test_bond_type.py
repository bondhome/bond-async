"""Unit tests for DeviceType."""

from bond_async.bond_type import BondType


def test_regexes():
    """Tests getting a BondType enum from Bond serial number"""
    assert BondType.BRIDGE_ZERMATT == BondType.from_serial("ZXBL12345")
    assert BondType.BRIDGE_ZERMATT == BondType.from_serial("ZZBL29913")

    assert BondType.BRIDGE_PRO == BondType.from_serial("ZPEA77140")
    assert BondType.BRIDGE_PRO == BondType.from_serial("ZPDK64712")

    assert BondType.BRIDGE_SNOWBIRD == BondType.from_serial("AJ12707")
    assert BondType.BRIDGE_SNOWBIRD == BondType.from_serial("BA12707")

    assert BondType.SBB_LIGHTS == BondType.from_serial("TADDAFA98593")
    assert BondType.SBB_LIGHTS == BondType.from_serial("TWCTAXX56966")

    assert BondType.SBB_CEILING_FAN == BondType.from_serial("KMBI10045")
    assert BondType.SBB_CEILING_FAN == BondType.from_serial("KXXX10044")
    assert BondType.SBB_CEILING_FAN == BondType.from_serial("KSMJCD54321")

    assert BondType.SBB_PLUG == BondType.from_serial("PPCTAXX88803")

    assert None == BondType.from_serial("garbage")
    assert None == BondType.from_serial("NOTASERIAL")


def test_is_sbb():
    """Tests if a Bond serial number is a SBB"""
    assert False == BondType.is_sbb_from_serial("ZXBL12345")
    assert False == BondType.is_sbb_from_serial("ZZBL29913")

    assert False == BondType.is_sbb_from_serial("ZPEA77140")
    assert False == BondType.is_sbb_from_serial("ZPDK64712")

    assert False == BondType.is_sbb_from_serial("AJ12707")
    assert False == BondType.is_sbb_from_serial("BA12707")

    assert True == BondType.is_sbb_from_serial("TADDAFA98593")
    assert True == BondType.is_sbb_from_serial("TWCTAXX56966")

    assert True == BondType.is_sbb_from_serial("KMBI10045")
    assert True == BondType.is_sbb_from_serial("KXXX10044")
    assert True == BondType.is_sbb_from_serial("KSMJCD54321")

    assert True == BondType.is_sbb_from_serial("PPCTAXX88803")

    assert False == BondType.is_sbb_from_serial("garbage")
    assert False == BondType.is_sbb_from_serial("NOTASERIAL")


def test_is_bridge():
    """Tests if a Bond serial number is a SBB"""
    assert True == BondType.is_bridge_from_serial("ZXBL12345")
    assert True == BondType.is_bridge_from_serial("ZZBL29913")

    assert True == BondType.is_bridge_from_serial("ZPEA77140")
    assert True == BondType.is_bridge_from_serial("ZPDK64712")

    assert True == BondType.is_bridge_from_serial("AJ12707")
    assert True == BondType.is_bridge_from_serial("BA12707")

    assert False == BondType.is_bridge_from_serial("TADDAFA98593")
    assert False == BondType.is_bridge_from_serial("TWCTAXX56966")

    assert False == BondType.is_bridge_from_serial("KMBI10045")
    assert False == BondType.is_bridge_from_serial("KXXX10044")
    assert False == BondType.is_bridge_from_serial("KSMJCD54321")

    assert False == BondType.is_bridge_from_serial("PPCTAXX88803")

    assert False == BondType.is_bridge_from_serial("garbage")
    assert False == BondType.is_bridge_from_serial("NOTASERIAL")
