from typing import Optional
from datetime import datetime
from datetime import time
from datetime import timedelta



class Clock:
    def __init__(self, increment: int = 5, synchronize: bool=False) -> None:
        self.__increment = increment
        self.__times = []
        self.__time_pointer = 0

        if increment < 1 and self.__scale == '-m':
            self.__increment = 1

        self.__build_clock(synchronize)

    def __build_clock(self, synchronize: bool) -> None:
        self.__times = Clock.times_in_24hours(self.__increment)

        if synchronize:
            self.__synchronize()

    def __synchronize(self) -> None:
        '''
            Changes the index of the clock time list to the nearest time
            in the clock ahead of current time.

            Ex: assume increment is 5 minutes
                current time = 12:05:24 -> time pointer set to index of 12:10:00
            :return: None
        '''
        current_time = datetime.now().time()

        # Because a clock is a circular list, reset to 0, if end is reached
        if self.__times[-1] < current_time:
            self.__time_pointer = 0
            return

        # if here then the time is between midnight and next day

        # This is an iterator and uses a "pointer" index to track the next
        # item to return
        time_idx = 0
        while self.__times[time_idx] < current_time:
            time_idx += 1

        self.__time_pointer = time_idx

    @staticmethod
    def times_in_24hours(increment: int=5) -> tuple:
        time_ = datetime(year=2022, month=1, day=1, hour=0, minute=0, second=0)
        end_of_day = datetime(year=2022, month=1, day=1, hour=23, minute=59, second=59)

        t_delta = timedelta(minutes=increment)

        times_in_day = []
        while time_ <= end_of_day:
            times_in_day.append(time_.time())
            time_ = time_ + t_delta

        return times_in_day

    @property
    def increment(self) -> int:
        return self.__increment

    def __iter__(self):
        return self

    def __next__(self) -> Optional[time]:
        '''
            This provides the next time in a circular list of times.

            :return: Optional[datetime.time]
        '''
        if not self.__times:
            raise StopIteration('Clock has no more times')

        next_time = self.__times[self.__time_pointer]
        self.__time_pointer = (self.__time_pointer + 1) % len(self.__times)

        return next_time
