from threading import Timer
from typing import Optional
from typing import Tuple
from twilio.rest import Client
from decouple import config

from .service_utils import Clock
from .db_access import get_db
from .db_access import execute_statement


class NotifierTimer(Timer):
    def __init__(self, clock_inc: int = 5) -> None:
        # create the clock first, so that is ensures valid increment
        self.__clock = Clock(increment=clock_inc, synchronize=True)

        # pass this instances __notify method to superclass __init__
        # to provide Timer functionality
        super().__init__(self.__clock.increment * 60, self.__notify)

        self.__next_time = next(self.__clock) # used to look ahead in time (and get data)

    def __notify(self) -> None:
        '''
            Provides the functionality of the timer.

            Obtain the next batch of patients to notify of medication
            pending administration, send notification that medication is due.
            :return: None
        '''

        # Get names and numbers of patients to notify
        notification_list = self.__patients_to_notify(admin_time=self.__next_time)

        # increment the next time to notify
        self.__next_time = next(self.__clock)

        client = Client(config('TWILIO_ACCOUNT_SID'), config('TWILIO_AUTH_TOKEN'))
        server_number = config('TWILIO_NUMBER')
        for notify_target in notification_list:
            client.messages.create(to=notify_target.mobile_number,
                                   from_=server_number,
                                   body=f'Hello, {notify_target.first_name}. Reminder from MedGuardian.')

    def __patients_to_notify(self) -> Tuple[tuple]:
        '''
            Query database for patients to notify if they have medication
            to be administered at
            :return:
        '''
        #####################################################
        ######NEED TO MAKE SURE ALL TIMES ARE CONVERTED TO TIME WHERE
        ######SERVER LIVES
        stmt = f'''
                    WITH contact_num_ids AS (
                        SELECT DISTINCT ct.contact_id FROM prescriptions_contacttimes ct
                        WHERE ct.id = (SELECT id FROM prescriptions_administrationtime
                                       WHERE value = {self.__next_time})
                    )
                    SELECT ci.mobile_phone, p.first_name FROM src_contactinformation ci
                    WHERE ci.id = ct.contact_id
                    INNER JOIN src_patient p ON p.contact_information_id = ci.id;
                '''

        result = execute_statement(get_db(), stmt)
        return list(result) if result else result
