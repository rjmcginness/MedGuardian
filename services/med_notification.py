import datetime
import time
from threading import Thread
from threading import Event
from typing import Optional
from typing import Tuple
from twilio.rest import Client
from decouple import config

# from .service_utils import Clock
# from .db_access import get_db
# from .db_access import execute_statement

from service_utils import Clock
from db_access import get_db
from db_access import execute_statement

#
# class NotifierTimer(Thread):
#     def __init__(self, event: Event, clock_inc: int = 0.5) -> None:
#         '''
#             :param clock_inc: the duration in minutes between
#             firings of notifications
#         '''
#         # create the clock first, so that is ensures valid increment
#         self.__clock = Clock(increment=clock_inc, synchronize=True)
#         self.__next_time = next(self.__clock)  # used to look ahead in time (and get data)
#
#         # pass the __notify method to superclass __init__
#         # as target to provide Timer functionality
#         super().__init__(target=self.__notify, args=(event,))
#
#     def __notify(self) -> None:
#         '''
#             Provides the functionality of the timer.
#
#             Obtain the next batch of patients to notify of medication
#             pending administration, send notification that medication is due.
#             :return: None
#         '''
#
#         increment = self.__clock.increment * 60
#
#         while not self.__event.is_set():
#             # Get names and numbers of patients to notify
#             notification_list = self.__patients_to_notify(admin_time=self.__next_time)
#
#             print('>>>>>>>>', notification_list)
#
#             # increment the next time to notify
#             self.__next_time = next(self.__clock)
#
#             # client = Client(config('TWILIO_ACCOUNT_SID'), config('TWILIO_AUTH_TOKEN'))
#             # server_number = config('TWILIO_NUMBER')
#             # for notify_target in notification_list:
#             #     client.messages.create(to=notify_target.mobile_number,
#             #                            from_=server_number,
#             #                            body=f'Hello, {notify_target.first_name}. Reminder from MedGuardian.')
#
#             time.sleep(self.)
#     def __patients_to_notify(self) -> Tuple[tuple]:
#         '''
#             Query database for patients to notify if they have medication
#             to be administered at
#             :return:
#         '''
#         #####################################################
#         ######NEED TO MAKE SURE ALL TIMES ARE CONVERTED TO TIME WHERE
#         ######SERVER LIVES
#         stmt = f'''
#                     WITH contact_num_ids AS (
#                         SELECT DISTINCT ct.contact_id FROM prescriptions_contacttimes ct
#                         WHERE ct.id = (SELECT id FROM prescriptions_administrationtime
#                                        WHERE value = {self.__next_time})
#                     )
#                     SELECT ci.mobile_phone, p.first_name FROM src_contactinformation ci
#                     WHERE ci.id = ct.contact_id
#                     INNER JOIN src_patient p ON p.contact_information_id = ci.id;
#                 '''
#
#         result = execute_statement(get_db(), stmt)
#         return list(result) if result else result

def patients_to_notify(admin_time: datetime.datetime.time) -> Tuple[tuple]:
    '''
                Query database for patients to notify if they have medication
                to be administered at admin_time
                :return: A Tuple of tuples, containing patient name and
                         mobile number
            '''
    #####################################################
    ######NEED TO MAKE SURE ALL TIMES ARE CONVERTED TO TIME WHERE
    ######SERVER LIVES
    stmt = f'''
                SELECT DISTINCT(ct.contact_id), ci.mobile_phone FROM prescriptions_contacttimes ct, src_contactinformation ci
                WHERE ct.administration_time_id = (SELECT pat.id FROM prescriptions_administrationtime pat
			    WHERE pat.value = TIME '{admin_time}') AND ci.id=ct.contact_id;

            '''

    result = execute_statement(get_db(), stmt, 'DB error in notification')
    return list(result) if result else result

if __name__ == '__main__':
    clock = Clock(synchronize=True)
    increment = clock.increment * 60
    next(clock)  # bump ahead a little

    while True:
        try:
            # Get names and numbers of patients to notify
            admin_time = next(clock)
            notification_list = patients_to_notify(admin_time=admin_time)

            client = Client(config('TWILIO_ACCOUNT_SID'), config('TWILIO_AUTH_TOKEN'))
            server_number = config('TWILIO_NUMBER')
            for notify_target in notification_list:
                client.messages.create(to=notify_target[1],
                                       from_=server_number,
                                       body=f'Hello! A reminder from MedGuardian.')

            time.sleep(increment)
        except KeyboardInterrupt:
            print('exited', datetime.datetime.now())
            exit()
