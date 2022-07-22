import pytest
from .service_utils import Clock
from datetime import datetime


def test_clock_daily_times():
    # get every 5 minutes
    daily_times = Clock.times_in_24hours()

    assert (12 * 24 == len(daily_times) and
            daily_times[0] == datetime(year=2022, month=1, day=1, hour=0, minute=0, second=0).time() and
            daily_times[-1] == datetime(year=2022, month=1, day=1, hour=23, minute=55, second=0).time()
           )