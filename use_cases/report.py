from adapters.repositories import UserBalanceRepository
from entities.entities import UserBalance
from settings import Settings
from use_cases import BaseInteractor

settings = Settings()


class ReportInteractor(BaseInteractor):

    async def execute(self, external_user_id: int) -> str:
        actual_balances = await UserBalanceRepository(self._db_session).get_actual_positions_by_user(
            UserBalance(external_user_id=external_user_id)
        )


        return [f"{i['currency']}: {i['amount']}" for i in actual_balances]
