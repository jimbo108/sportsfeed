from enum import Enum


class ExternalIdentifierType(Enum):
    NUMERIC = 1
    STRING = 2

class FixtureStatusIds(Enum):
    FINISHED = 0
    IN_PLAY = 1
    PAUSED = 2
    POSTPONED = 3
    SCHEDULED = 4
    SUSPENDED = 5
    AWARDED = 6
    CANCELED = 7
