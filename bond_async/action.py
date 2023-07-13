"""Typed helpers for executable actions for Bond Local API."""

from enum import IntEnum
from typing import Any


class Direction(IntEnum):
    """Direction enumeration for supported fan directions."""

    FORWARD = 1
    REVERSE = -1


class Action:
    """Namespace for Bond API action helpers and constants."""

    # General actions
    STOP = "Stop"
    TURN_ON = "TurnOn"
    TURN_OFF = "TurnOff"
    TOGGLE_POWER = "TogglePower"
    SET_TIMER = "SetTimer"
    SWITCH_MODE = "SwitchMode"
    SET_STATE_BELIEF = "state"
    HOME_SHIELD_ON = "HomeShieldOn"
    HOME_SHIELD_OFF = "HomeShieldOff"
    HOME_SHIELD_TOGGLE = "HomeShieldToggle"

    # Lights
    TURN_LIGHT_ON = "TurnLightOn"
    TURN_LIGHT_OFF = "TurnLightOff"
    TOGGLE_LIGHT = "ToggleLight"
    SET_BRIGHTNESS = "SetBrightness"
    INCREASE_BRIGHTNESS = "IncreaseBrightness"
    DECREASE_BRIGHTNESS = "DecreaseBrightness"
    START_DIMMER = "StartDimmer"
    TURN_UP_LIGHT_ON = "TurnUpLightOn"
    TURN_DOWN_LIGHT_ON = "TurnDownLightOn"
    TURN_UP_LIGHT_OFF = "TurnUpLightOff"
    TURN_DOWN_LIGHT_OFF = "TurnDownLightOff"
    TOGGLE_UP_LIGHT = "ToggleUpLight"
    TOGGLE_DOWN_LIGHT = "ToggleDownLight"
    START_UP_LIGHT_DIMMER = "StartUpLightDimmer"
    START_DOWN_LIGHT_DIMMER = "StartDownLightDimmer"
    START_INCREASING_BRIGHTNESS = "StartIncreasingBrightness"
    START_DECREASING_BRIGHTNESS = "StartDecreasingBrightness"
    SET_UP_LIGHT_BRIGHTNESS = "SetUpLightBrightness"
    SET_DOWN_LIGHT_BRIGHTNESS = "SetDownLightBrightness"
    INCREASE_UP_LIGHT_BRIGHTNESS = "IncreaseUpLightBrightness"
    DECREASE_UP_LIGHT_BRIGHTNESS = "DecreaseUpLightBrightness"
    INCREASE_DOWN_LIGHT_BRIGHTNESS = "IncreaseDownLightBrightness"
    DECREASE_DOWN_LIGHT_BRIGHTNESS = "DecreaseDownLightBrightness"
    CYCLE_UP_LIGHT_BRIGHTNESS = "CycleUpLightBrightness"
    CYCLE_DOWN_LIGHT_BRIGHTNESS = "CycleDownLightBrightness"
    CYCLE_BRIGHTNESS = "CycleBrightness"
    CYCLE_COLOR_TEMP = "CycleColorTemp"
    SET_COLOR_TEMP = "SetColorTemp"
    CYCLE_COLOR_TEMP_PRESET = "CycleColorTempPreset"
    DECREASE_COLOR_TEMP = "DecreaseColorTemp"
    INCREASE_COLOR_TEMP = "IncreaseColorTemp"

    # Fans
    BREEZE_OFF = "BreezeOff"
    BREEZE_ON = "BreezeOn"
    DECREASE_SPEED = "DecreaseSpeed"
    DIM_MODE = "DimMode"
    INCREASE_SPEED = "IncreaseSpeed"
    OEM_HOME_AWAY = "OEMHomeAway"
    OEM_RANDOM = "OEMRandom"
    OEM_RANDOM_TOGGLE = "OEMRandomToggle"
    OEM_TIMER = "OEMTimer"
    OEM_WALK_AWAY = "OEMWalkAway"
    SET_BREEZE = "SetBreeze"
    SET_DIRECTION = "SetDirection"
    SET_SPEED = "SetSpeed"
    TOGGLE_DIRECTION = "ToggleDirection"
    TOGGLE_LIGHT_TEMP = "ToggleLightTemp"

    # Fireplaces
    INCREASE_TEMPERATURE = "IncreaseTemperature"
    DECREASE_TEMPERATURE = "DecreaseTemperature"
    SET_FP_FAN = "SetFpFan"
    TURN_FP_FAN_ON = "TurnFpFanOn"
    TURN_FP_FAN_OFF = "TurnFpFanOff"
    INCREASE_FLAME = "IncreaseFlame"
    DECREASE_FLAME = "DecreaseFlame"
    SET_FLAME = "SetFlame"

    # Motorized Shades
    CLOSE = "Close"
    CLOSE_NEXT = "CloseNext"
    DECREASE_POSITION = "DecreasePosition"
    ESC = "Esc"
    HOLD = "Hold"
    INCREASE_POSITION = "IncreasePosition"
    LONG_CLOSE = "LongClose"
    LONG_HOLD = "LongHold"
    LONG_OPEN = "LongOpen"
    LONG_PAIR = "LongPair"
    OPEN = "Open"
    OPEN_NEXT = "OpenNext"
    PAIR = "Pair"
    PRESET = "Preset"
    SAVE_LIMIT_BOTTOM_OEM = "SaveLimitBottomOEM"
    SAVE_LIMIT_TOP_OEM = "SaveLimitTopOEM"
    SET_LIMIT_BOTTOM_OEM = "SetLimitBottomOEM"
    SET_LIMIT_TOP_OEM = "SetLimitTopOEM"
    SET_POSITION = "SetPosition"
    TILT_CLOSE = "TiltClose"
    TILT_LEFT = "TiltLeft"
    TILT_LEFT_LONG = "TiltLeftLong"
    TILT_OPEN = "TiltOpen"
    TILT_RIGHT = "TiltRight"
    TILT_RIGHT_LONG = "TiltRightLong"
    TILT_STOP = "TiltStop"
    TOGGLE_OPEN = "ToggleOpen"

    def __init__(self, name: str, argument: Any = None):
        self._name = name
        if self._name == Action.SET_STATE_BELIEF:
            self._argument = {} if argument is None else argument
        else:
            self._argument = {} if argument is None else {"argument": argument}

    def __eq__(self, other: "Action"):
        return self.name == other.name and self.argument == other.argument

    @staticmethod
    def turn_on() -> "Action":
        """Turn device on (usually power)."""
        return Action(Action.TURN_ON)

    @staticmethod
    def turn_off() -> "Action":
        """Turn device off (usually power)."""
        return Action(Action.TURN_OFF)

    @staticmethod
    def open() -> "Action":
        """Open cover."""
        return Action(Action.OPEN)

    @staticmethod
    def close() -> "Action":
        """Close cover."""
        return Action(Action.CLOSE)

    @staticmethod
    def tilt_open() -> "Action":
        """Tilt open cover."""
        return Action(Action.TILT_OPEN)

    @staticmethod
    def tilt_close() -> "Action":
        """Tilt close cover."""
        return Action(Action.TILT_CLOSE)

    @staticmethod
    def hold() -> "Action":
        """Hold cover."""
        return Action(Action.HOLD)

    @staticmethod
    def set_speed(speed: int) -> "Action":
        """Sets fan rotation to a provided speed."""
        return Action(Action.SET_SPEED, speed)

    @staticmethod
    def set_speed_belief(speed: int) -> "Action":
        """Sets fan rotation to a provided speed."""
        return Action(Action.SET_STATE_BELIEF, {"speed": speed})

    @staticmethod
    def set_direction(direction: Direction) -> "Action":
        """Sets fan rotation direction."""
        return Action(Action.SET_DIRECTION, direction.value)

    @staticmethod
    def turn_light_on() -> "Action":
        """Turns on the fan light."""
        return Action(Action.TURN_LIGHT_ON)

    @staticmethod
    def turn_light_off() -> "Action":
        """Turns off the fan light."""
        return Action(Action.TURN_LIGHT_OFF)

    @staticmethod
    def set_light_state_belief(state: bool) -> "Action":
        """Sets light state belief, true or false."""
        return Action(Action.SET_STATE_BELIEF, {"light": int(state)})

    @staticmethod
    def set_power_state_belief(state: bool) -> "Action":
        """Sets light state belief, true or false."""
        return Action(Action.SET_STATE_BELIEF, {"power": int(state)})

    @staticmethod
    def set_brightness(brightness: int) -> "Action":
        """Sets brightness of the light as percentage value, 1-100."""
        return Action(Action.SET_BRIGHTNESS, brightness)

    @staticmethod
    def set_color_temperature(temperature: int) -> "Action":
        """Sets color temperature of the light in Kelin. Resolution: 100 K."""
        return Action(Action.SET_COLOR_TEMP, temperature)

    @staticmethod
    def increase_color_temperature(temperature: int) -> "Action":
        """Increases color temperature a specified number of degrees K. Implicitly turn Light on."""
        return Action(Action.INCREASE_COLOR_TEMP, temperature)

    @staticmethod
    def decrease_color_temperature(temperature: int) -> "Action":
        """Decreases color temperature a specified number of degrees K. Implicitly turn Light on."""
        return Action(Action.DECREASE_COLOR_TEMP, temperature)

    @staticmethod
    def set_brightness_belief(brightness: int) -> "Action":
        """Sets brightness belief of the light as percentage value, 1-100."""
        return Action(Action.SET_STATE_BELIEF, {"brightness": brightness})

    @staticmethod
    def set_flame(flame: int) -> "Action":
        """Sets the flame to given intensity in percent."""
        return Action(Action.SET_FLAME, flame)

    @staticmethod
    def set_position(position: int) -> "Action":
        """Sets shade position percentage from 0 (open) to 100 (closed)."""
        return Action(Action.SET_POSITION, position)

    @staticmethod
    def increase_position(position: int) -> "Action":
        """Closes the device by the specified percentage of the full range."""
        return Action(Action.INCREASE_POSITION, position)

    @staticmethod
    def decrease_position(position: int) -> "Action":
        """Opens the device by the specified percentage of the full range."""
        return Action(Action.DECREASE_POSITION, position)

    @property
    def name(self) -> str:
        """Return name of this action."""
        return self._name

    @property
    def argument(self) -> dict:
        """Return optional argument for this action."""
        return self._argument
