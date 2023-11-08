from unittest.mock import Mock, patch, AsyncMock

import pytest

from entities.entities import UserRequestStatusEnum, ExchangeRequest
from use_cases.uncategorized import UncategorizedInteractor


@pytest.fixture()
def exchange_request_repository():
    with patch('use_cases.uncategorized.ExchangeRequestRepository') as er:
        er.return_value = Mock(
            create_exchange_request=AsyncMock(),
        )
        yield er


@pytest.mark.asyncio
async def test_success(exchange_request_repository, db_session, logger, message_factory):
    message = message_factory()
    result = await UncategorizedInteractor(db_session).execute(message)
    assert result == 'Ваше сообщение зарегистрировано и в скором времени мы вернемся к вам с ответом.'

    entity = ExchangeRequest(
        msg_id=message.id,
        external_user_id=message.external_user_id,
        chat_id=message.chat_id,
        status=UserRequestStatusEnum.need_moderation.value,
        msg_text=message.text
    )

    exchange_request_repository.return_value.create_exchange_request.assert_called_with(entity)
