import asyncio
from asyncio import AbstractEventLoop
from typing import Optional, List

import asyncpg

from settings import Settings


class Database:
    def __init__(
        self,
        name: Optional[str],
        user: Optional[str],
        password: Optional[str],
        host: Optional[str],
        port: Optional[str],
        loop: AbstractEventLoop,
    ) -> None:
        self.name = name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.loop = loop
        self.pool = loop.run_until_complete(
            asyncpg.create_pool(
                database=name,
                user=user,
                password=password,
                host=host,
                port=port,
                max_inactive_connection_lifetime=3
            )
        )

    async def close_connection(self) -> None:
        await self.pool.close()

    async def execute(self, sql: str) -> None:
        await self.pool.execute(sql)

    async def fetch(self, sql: str) -> List[str]:
        return await self.pool.fetch(sql)

    async def fetchrow(self, sql: str):
        return await self.pool.fetchrow(sql)

    async def fetchval(self, sql: str):
        return await self.pool.fetchval(sql)


settings = Settings()

db = Database(
    name=settings.db_name,
    user=settings.db_user,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port,
    loop=asyncio.get_event_loop(),
)
