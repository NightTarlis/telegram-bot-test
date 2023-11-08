import datetime

from adapters.repositories.exchange_request import ExchangeRequestRepository
from entities.dto import MessageDTO
from entities.entities import ExchangeRequest, UserRequestStatusEnum
from settings import Settings
from use_cases import BaseInteractor

settings = Settings()


class UncategorizedInteractor(BaseInteractor):

    async def execute(self, message: MessageDTO) -> str:
        entity = ExchangeRequest(
            msg_id=message.id,
            external_user_id=message.external_user_id,
            chat_id=message.chat_id,
            status=UserRequestStatusEnum.need_moderation.value,
            msg_text=message.text
        )

        await ExchangeRequestRepository(self._db_session).create_exchange_request(entity)

        return 'Ваше сообщение зарегистрировано и в скором времени мы вернемся к вам с ответом.'

