import datetime
import time
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



def patients_to_notify(db, admin_time: datetime.datetime.time) -> Tuple[tuple]:
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

    result = execute_statement(db, stmt, 'DB error in notification')
    return list(result) if result else result

if __name__ == '__main__':
    db = get_db()
    clock = Clock(synchronize=True)
    increment = clock.increment * 60
    next(clock)  # bump ahead a little

    while True:
        try:
            # Get names and numbers of patients to notify
            admin_time = next(clock)
            notification_list = patients_to_notify(db, admin_time=admin_time)

            # if there are numbers to notify, do so
            if notification_list:
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
