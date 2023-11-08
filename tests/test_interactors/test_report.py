from unittest.mock import Mock, patch, AsyncMock

import pytest

from entities.entities import UserBalance
from use_cases.report import ReportInteractor


@pytest.fixture()
def user_balance_repository():
    with patch('use_cases.report.UserBalanceRepository') as er:
        er.return_value = Mock(
            get_actual_positions_by_user=AsyncMock(
                return_value=[{'currency': 'usd', 'amount': 1}, {'currency': 'rub', 'amount': 2}]
            ),
        )
        yield er


@pytest.mark.asyncio
async def test_success_empty(user_balance_repository, db_session, user_factory):
    user = user_factory(user_id=1)
    result = await ReportInteractor(db_session).execute(user)
    assert result == ['usd: 1', 'rub: 2']

    user_balance_repository.return_value.get_actual_positions_by_user.assert_called_with(
        UserBalance(external_user_id=user.id)
    )
