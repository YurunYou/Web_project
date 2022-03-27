from enum import Enum


class DeviceStatus(Enum):
    Available = 'available'
    Broken = 'broken'
    Unavailable = 'unavailable'
