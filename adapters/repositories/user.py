from adapters.repositories import BaseRepository
from entities import User


class UserRepository(BaseRepository):
    async def create_user(self, entity: User) -> None:
        await self._db_session.execute(
            f'''insert into users(external_id, username, fullname) values
            ({entity.external_id}, '{entity.username}', '{entity.fullname}');'''
        )

    async def check_user_exists(self, entity: User) -> bool:
        return bool(await self._db_session.fetchval(f'select 1 from users where external_id = {entity.external_id};'))
