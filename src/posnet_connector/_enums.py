from enum import IntEnum


class FooterEnding(IntEnum):
    CUT_WITH_FEED = 0  # with feed and cut (default)
    FEED_NO_CUT = 1  # with feed but without cut
    CUT_NO_FEED = 2  # without feed and cut


class DisplayTarget(IntEnum):
    CUSTOMER = 0
    OPERATOR = 1


class BacklightMode(IntEnum):
    ALWAYS_OFF = 0
    ALWAYS_ON = 1
    ON_AC_POWER = 2
