import logging
from decimal import Decimal

from adapters.repositories import UserBalanceRepository
from entities.dto import UserDTO
from entities.entities import UserBalance
from settings import Settings
from use_cases import BaseInteractor

settings = Settings()

logger = logging.getLogger(__name__)


class ReportInteractor(BaseInteractor):

    async def execute(self, user: UserDTO) -> str:
        actual_balances = await UserBalanceRepository(self._db_session).get_actual_positions_by_user(
            UserBalance(external_user_id=user.id)
        )

        return [f"{i['currency']}: {round(Decimal(i['amount']), 6)}" for i in actual_balances]
