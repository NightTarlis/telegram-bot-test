from unittest.mock import Mock, patch, AsyncMock

import pytest

from entities.entities import UserBalance, UserRequestStatusEnum, ExchangeRequest
from use_cases.exchange_request import ExchangeRequestInteractor


@pytest.fixture()
def exchange_request_repository_mock():
    with patch('use_cases.exchange_request.ExchangeRequestRepository.create_exchange_request') as er:
        er.return_value = AsyncMock()
        yield er


@pytest.fixture()
def user_balance_repository_mock():
    with patch('use_cases.exchange_request.UserBalanceRepository') as er:
        er.return_value = Mock(
            check_can_user_exchange_currency=AsyncMock(return_value=True),
            update_user_balance=AsyncMock(),
        )
        yield er


@pytest.fixture()
def price_service_mock():
    with patch('use_cases.exchange_request.PriceRequestService') as er:
        er.return_value = Mock(
            get_exchange_price=AsyncMock(return_value=34000),
            exchange=AsyncMock(return_value=True),
        )
        yield er


@pytest.mark.asyncio
async def test_but_btc_from_usdt(
        db_session, message_factory, price_service_mock, user_balance_repository_mock, exchange_request_repository_mock
):
    message = message_factory(text='buy 1 btc/usdt')
    result = await ExchangeRequestInteractor(db_session).execute(message)
    currency_from, currency_to, amount = 'btc', 'usdt', 34000

    user_balance = UserBalance(external_user_id=message.external_user_id, currency=currency_to, amount=amount)

    user_balance_repository_mock().check_can_user_exchange_currency.assert_called_with(user_balance)
    price_service_mock().get_exchange_price.assert_called_with(currency_from, currency_to)
    price_service_mock().exchange.assert_called_with(currency_to, currency_from, amount)

    assert result == 'Сделка по обмену usdt на btc состоялась, по цене 34000'
