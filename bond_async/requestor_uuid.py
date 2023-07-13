from enum import Enum


class RequestorUUID(Enum):
    # These are the existing requestor IDs that are already allocated
    TEST = 0x00
    # Only allow requestor IDs greater than 0xA0
    ANONYMOUS = 0xFF
    HOME_ASSISTANT = 0xA0

    # method that returns if a given hex requestor is allowed
    def is_allowed(self) -> bool:
        return self.value >= 0xA0

    def hex_value(self) -> str:
        return f"{self.value:02x}"
