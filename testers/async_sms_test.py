from datetime import datetime
from datetime import timedelta
from datetime import time
from time import sleep
from threading import Timer
from typing import Optional
from twilio.rest import Client
from decouple import config
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
            raise StopIteration('Clock has no more times')

        next_time = self.__times[self.__time_pointer]
        self.__time_pointer = (self.__time_pointer + 1) % len(self.__times)

        return next_time


class NotifierTimer(Timer):
    def __init__(self, clock_inc: int = 5) -> None:
        self.__clock = Clock(increment=clock_inc)
        super().__init__(self.__clock.increment*60, self.__notify)
        self.__next_time = None

    def __notify(self) -> None:
        # Get prescritions with this admin time
        admin_time = next(self.__clock)
        prescriptions = []

        client = None

        if not prescriptions:
            return

        client = Client(config('TWILIO_ACCOUNT_SID'), config('TWILIO_AUTH_TOKEN'))
        server_number = config('TWILIO_NUMBER')
        for rx in prescriptions:
            
            client.messages.create()



if __name__ == '__main__':
    clock = Clock()

    for _ in range(500):
        print(next(clock))
