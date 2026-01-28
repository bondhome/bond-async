"""Bond Device type enumeration."""


class DeviceType:
    """Bond Device type enumeration."""

    CEILING_FAN = "CF"
    MOTORIZED_SHADES = "MS"
    FIREPLACE = "FP"
    AIR_CONDITIONER = "AC"
    GARAGE_DOOR = "GD"
    BIDET = "BD"
    LIGHT = "LT"
    GENERIC_DEVICE = "GX"
    SWITCH = "SW"
    HEATER = "HT"

    @staticmethod
    def is_fan(device_type: str) -> bool:
        """Checks if specified device type is a fan."""
        return device_type == DeviceType.CEILING_FAN

    @staticmethod
    def is_shades(device_type: str) -> bool:
        """Checks if specified device type is shades."""
        return device_type == DeviceType.MOTORIZED_SHADES

    @staticmethod
    def is_fireplace(device_type: str) -> bool:
        """Checks if specified device type is fireplace."""
        return device_type == DeviceType.FIREPLACE

    @staticmethod
    def is_air_conditioner(device_type: str) -> bool:
        """Checks if specified device type is air conditioner."""
        return device_type == DeviceType.AIR_CONDITIONER

    @staticmethod
    def is_garage_door(device_type: str) -> bool:
        """Checks if specified device type is garage door."""
        return device_type == DeviceType.GARAGE_DOOR

    @staticmethod
    def is_bidet(device_type: str) -> bool:
        """Checks if specified device type is bidet."""
        return device_type == DeviceType.BIDET

    @staticmethod
    def is_light(device_type: str) -> bool:
        """Checks if specified device type is light."""
        return device_type == DeviceType.LIGHT

    @staticmethod
    def is_generic(device_type: str) -> bool:
        """Checks if specified device type is generic."""
        return device_type == DeviceType.GENERIC_DEVICE

    @staticmethod
    def is_switch(device_type: str) -> bool:
        """Checks if specified device type is switch."""
        return device_type == DeviceType.SWITCH

    @staticmethod
    def is_heater(device_type: str) -> bool:
        """Checks if specified device type is heater."""
        return device_type == DeviceType.HEATER
