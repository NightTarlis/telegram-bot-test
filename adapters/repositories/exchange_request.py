import re
from decimal import Decimal
from typing import List, Optional

from adapters.repositories.repository import BaseRepository
from entities.entities import ExchangeRequest, UserBalance


class ExchangeRequestRepository(BaseRepository):

    @staticmethod
    async def parse_message(msg: str) -> List[Optional[str]]:
        """
        Parse income message and return amount and currencies

        :param msg: - message for parsing
        :return: list with amount, from which currency to do operation, to which currency to do operation
        """

        pattern = r'(\w+)\s+([\d.]+)\s+([A-Za-z]+)\s*[-/.\\_ ]\s*([A-Za-z]+)'
        match = re.match(pattern, msg)
        if match:
            return match.group(1).lower(), Decimal(match.group(2)), match.group(3), match.group(4)
        else:
            return None, None, None, None

    async def create_exchange_request(self, entity: ExchangeRequest):

        await self._db_session.execute(
            f'''insert into exchange_requests(
                msg_id, external_user_id, chat_id, status, msg_text,
                currency_from, currency_to, amount, created_at, updated_at,
                price
            ) values
            (
                {entity.msg_id}, {entity.external_user_id}, {entity.chat_id}, '{entity.status}', '{entity.msg_text}',
                '{entity.currency_from}', '{entity.currency_to}', {entity.amount}, '{entity.created_at}'::timestamp,
                '{entity.updated_at}'::timestamp, {entity.price}
            );'''
        )

    async def get_data_for_week(self, entity: UserBalance):

        await self._db_session.fetch(
            f'''
                select sum(amount), currency_from, currency_to 
                from exchange_requests 
                where external_user_id = {entity.external_user_id} 
                  and status = 'finished' 
                group by currency_from, currency_to;
            '''
        )
