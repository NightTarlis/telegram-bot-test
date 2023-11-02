from unittest.mock import Mock, patch, AsyncMock

import pytest

from use_cases.exchange_request import ExchangeRequestInteractor


@pytest.fixture()
def message_mock():
    with patch('use_cases.exchange_request.ExchangeRequestRepository.parse_message') as b:
        b.return_value = ['sell', '1', '1', '1']
        yield b


@pytest.fixture()
def price_service_mock():
    with patch('use_cases.exchange_request.PriceRequestService') as m:
        m.return_value = AsyncMock(get_exchange_price=1)
        yield m



@pytest.mark.asyncio
async def test_exchange(message_mock, db_session, price_service_mock):
    result = await ExchangeRequestInteractor(db_session).execute(Mock(), 1)
    assert result == ['usd: 1', 'rub: 2']


