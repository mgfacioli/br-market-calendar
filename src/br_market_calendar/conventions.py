from __future__ import annotations

from enum import StrEnum


class BusinessDayConvention(StrEnum):
    """
    Business day adjustment conventions.
    """

    FOLLOWING = "following"
    PRECEDING = "preceding"
    MODIFIED_FOLLOWING = "modified_following"
    MODIFIED_PRECEDING = "modified_preceding"
    UNADJUSTED = "unadjusted"
