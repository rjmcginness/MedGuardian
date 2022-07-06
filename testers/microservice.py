# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 12:32:13 2022

@author: Robert J McGinness
"""

import sqlalchemy as sa
from datetime import time


class DBWrapper:
    def __init__(self, db_url: str) -> None:
        self.url = db_url
        self.__engine = sa.create_engine(db_url, echo=True, future=True)
    
    @property
    def engine(self):
        return self.__engine
    

class NotificationSet(DBWrapper):
    def get(self, administration_time: time) -> list:
        ''' Encapsulates the database query and returns 
            a list of key-value pairs of patient name 
            and mobile device number
        '''
        
        ######NEED TO INCORPORATE TIMEZONES OF USERS
        ######OR CONVERT ALL USER TIMES TO TIME ZONE OF SERVER
        
        # From the administration time argument get the prescriptions
        # as a subquery, then get the patient name and mobile device
        # contact information
        query_str = f'''
                        SELECT p.first_name, c.mobile FROM users_patient p
                        INNER JOIN src_contact_information c
                        ON p.contact_information_id = c.id
                        WHERE p.id IN (
                            SELECT pr.patient_id FROM prescriptions_prescription as pr
                            INNER JOIN prescriptions_prescription_admin_time at
                            ON pr.id = at.prescription_id
                            WHERE at.value == {administration_time}
                        )
                    '''
        # execute query on database
        results = None
        with self.engine.connect() as conn:
            results = conn.execute(sa.text(query_str))
        
        # pack results into list of key-value pairs
        patients_to_notify = []
        for row in results:
            patients_to_notify.append({row.first_name: row.mobile})
        
        return patients_to_notify

