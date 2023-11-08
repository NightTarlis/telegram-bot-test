from unittest.mock import patch, Mock, AsyncMock

import pytest

from entities import User
from use_cases.start import StartInteractor


@pytest.fixture()
def user_repository_mock():
    with patch('use_cases.start.UserRepository') as ur:
        ur.return_value = Mock(
            check_user_exists=AsyncMock(
                return_value=True
            ),
            create_user=AsyncMock(
                return_value=True
            ),
        )
        yield ur


@pytest.fixture()
def user_balance_repository_mock():
    with patch('use_cases.start.UserBalanceRepository') as er:
        er.return_value = Mock(create_base_balance=AsyncMock())
        yield er


@pytest.mark.asyncio
async def test_start_new_user(db_session, user_factory, user_repository_mock, user_balance_repository_mock):
    user_repository_mock.return_value = Mock(
        check_user_exists=AsyncMock(
            return_value=False
        ),
        create_user=AsyncMock()
    )
    user = user_factory()
    result = await StartInteractor(db_session).execute(user)
    print(result)
    assert not result.startswith(f'Здравствуйте, {user.first_name}!')
    assert '10000 usdt' in result
    user_balance_repository_mock.create_base_balance.assert_not_called()
    user_repository_mock.create_user.assert_not_called()


@pytest.mark.asyncio
async def test_start_exist_user(
        db_session, user_factory, user_repository_mock, user_balance_repository_mock
):
    user = user_factory()
    result = await StartInteractor(db_session).execute(user)

    assert not result.startswith('Здравствуйте, ')
    assert '10000 usdt' not in result
    user_repository_mock.create_user.assert_not_called()
    user_balance_repository_mock.create_user.assert_not_called()
