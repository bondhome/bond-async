"""Bond type enumeration."""
import re
from enum import Enum

regexes = {
    "bridge_snowbird": r"^[A-C]\w*$",
    "bridge_zermatt": r"^Z(Z|X)\w*$",
    "bridge_pro": r"^ZP\w*$",
    "sbb_lights": r"^T\w*$",
    "sbb_ceiling_fan": r"^K\w*$",
    "sbb_plug": r"^P\w*$",
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
        """Checks if BondType is a Smart by Bond product."""
        return self.value.startswith("sbb_")

    def is_bridge(self) -> bool:
        """Checks if BondType is a Bond Bridge/Bond Bridge Pro."""
        return self.value.startswith("bridge_")

    @classmethod
    def from_serial(cls, serial: str):
        """Returns a BondType for a serial number"""
        for (bond_type, regex) in regexes.items():
            if re.search(regex, serial):
                return cls(bond_type)
        return None

    @staticmethod
    def is_sbb_from_serial(serial: str) -> bool:
        """Checks if specified Bond serial number is a Smart by Bond product."""
        bond_type = BondType.from_serial(serial)
        if bond_type:
            return bond_type.is_sbb()
        return False

    @staticmethod
    def is_bridge_from_serial(serial: str) -> bool:
        """Checks if specified Bond serial number is a Bond Bridge."""
        bond_type = BondType.from_serial(serial)
        if bond_type:
            return bond_type.is_bridge()
        return False
