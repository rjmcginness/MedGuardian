from datetime import datetime
from datetime import timedelta
from datetime import time
from threading import Thread
from typing import Optional
# from prescriptions.models import PrescriptionAdminTime


class Clock:
    def __init__(self, increment: int = 5) -> None:
        self.__increment = increment
        self.__times = []
        self.__time_pointer = 0

        if increment < 1 and self.__scale == '-m':
            self.__increment = 1

        self.__build_clock()

    def __build_clock(self) -> None:
        time_ = datetime(year=2022, month=1, day=1, hour=0, minute=0, second=0)
        end_of_day = datetime(year=2022, month=1, day=1, hour=23, minute=59, second=59)

        t_delta = timedelta(minutes=self.__increment)

        while time_ <= end_of_day:
            self.__times.append(time_.time())
            time_ = time_ + t_delta

    @property
    def increment(self) -> int:
        return self.__increment

    def __iter__(self):
        return self

    def __next__(self) -> Optional[time]:
        if not self.__times:
            return None

        next_time = self.__times[self.__time_pointer]
        self.__time_pointer = (self.__time_pointer + 1) % len(self.__times)

        return next_time


class NotifierThread(Thread):
    def __init__(self) -> None:
        super().__init__()

    def run(self):
        super().run()


if __name__ == '__main__':
    clock = Clock()

    for _ in range(500):
        print(next(clock))
