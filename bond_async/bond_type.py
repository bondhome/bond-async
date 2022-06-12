"""Bond type enumeration."""
from enum import Enum
import re

regexes = {
    "bridge_snowbird": "^[A-C]\w*$",
    "bridge_zermatt": "^Z(Z|X)\w*$",
    "bridge_pro": "^ZP\w*$",
    "sbb_lights": "^T\w*$",
    "sbb_ceiling_fan": "^K\w*$",
    "sbb_plug": "^P\w*$",
}


class BondType(Enum):
    """Bond type enumeration."""

    BRIDGE_SNOWBIRD = "bridge_snowbird"
    BRIDGE_ZERMATT = "bridge_zermatt"
    BRIDGE_PRO = "bridge_pro"
    SBB_LIGHTS = "sbb_lights"
    SBB_CEILING_FAN = "sbb_ceiling_fan"
    SBB_PLUG = "sbb_plug"

    def is_sbb(self) -> bool:
        return self.value.startswith("sbb_")

    def is_bridge(self) -> bool:
        return self.value.startswith("bridge_")

    @classmethod
    def from_serial(cls, serial: str):
        """Returns a BondType for a serial number"""
        for type in regexes:
            if re.search(regexes[type], serial):
                return cls(type)
        return None

    @staticmethod
    def is_sbb_from_serial(serial: str) -> bool:
        """Checks if specified Bond serial number is a Smart by Bond product."""
        bondType = BondType.from_serial(serial)
        if bondType:
            return bondType.is_sbb()
        else:
            return False

    @staticmethod
    def is_bridge_from_serial(serial: str) -> bool:
        """Checks if specified Bond serial number is a Bond Bridge."""
        bondType = BondType.from_serial(serial)
        if bondType:
            return bondType.is_bridge()
        else:
            return False
