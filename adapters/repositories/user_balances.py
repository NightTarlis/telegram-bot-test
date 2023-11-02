from adapters.repositories.repository import BaseRepository
from entities.entities import UserBalance


class UserBalanceRepository(BaseRepository):

    async def create_base_balance(self, entity: UserBalance) -> None:
        await self._db_session.execute(
            f'''insert into user_balances(external_user_id, currency, amount) values
            ({entity.external_user_id}, '{entity.currency}', {entity.amount}::numeric);'''
        )

    async def check_can_user_exchange_currency(self, entity: UserBalance) -> bool:
        return bool(await self._db_session.fetchval(
            f'''
            select 1
            from user_balances
            where external_user_id = {entity.external_user_id}
              and currency = '{entity.currency}'
              and amount >= {entity.amount};
            '''
        ))

    async def get_actual_positions_by_user(self, entity: UserBalance) -> bool:

        # fixme: вместо этого должен быть запрос вот в этом направлении, но не успеваю придумать
        # select er1.price - er.price, er.currency_from
        # from exchange_requests er
        # left join exchange_requests er1 on er1.currency_to = er.currency_from
        # where er.status = 'finished';

        return await self._db_session.fetch(
            f'''
                select currency, round(amount, 10) as amount
                from user_balances
                where external_user_id = {entity.external_user_id};
            '''
        )

    async def update_user_balance(self, entity: UserBalance):
        await self._db_session.execute(
            f'''
                insert into user_balances(external_user_id, currency, amount) values
                ({entity.external_user_id}, '{entity.currency}', {entity.amount})
                on CONFLICT (external_user_id, currency) do update set amount = user_balances.amount + {entity.amount};
            '''
        )
