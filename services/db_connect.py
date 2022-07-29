"""
    Thin wrapper around a sqlalchemy engine, used to simplify
    db interactions.
"""

import sqlalchemy as sa


class DBWrapperError(Exception):
    pass


class DBWrapper:

    def __init__(self, db_url: str, echo=False) -> None:
        self.url = db_url
        self.__engine = sa.create_engine(db_url, echo=echo, future=True)


    @property
    def engine(self):
        return self.__engine

    def execute_statement(self, stmt: str, commit=False):
        try:
            with self.__engine.begin() as conn:

                stmt = sa.text(stmt)
                result = conn.execute(stmt)
        except sa.exc.DBAPIError as e:
            raise DBWrapperError(e)

        return result

    def close(self) -> None:
        self.engine.close()

def make_db_url(dialect, driver, user, password, host, port, name) -> str:
    return dialect + '+' + driver + '://' + user + ':' + password + '@' + host + ':' + port + '/' + name
