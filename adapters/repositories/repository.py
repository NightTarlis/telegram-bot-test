from abc import ABC

from asyncpg import Connection


class BaseRepository(ABC):
    _db_session = None

    def __init__(self, db_session: Connection):
        self._db_session = db_session
