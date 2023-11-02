import datetime

from adapters.repositories.exchange_request import ExchangeRequestRepository
from entities.entities import ExchangeRequest, UserRequestStatusEnum
from settings import Settings
from use_cases import BaseInteractor

settings = Settings()


class UncategorizedInteractor(BaseInteractor):

    async def execute(self, msg_id: int, chat_id: int, msg_text: str, external_user_id: int) -> str:
        entity = ExchangeRequest(
            msg_id=msg_id,
            external_user_id=external_user_id,
            chat_id=chat_id,
            status=UserRequestStatusEnum.need_moderation.value,
            msg_text=msg_text
        )

        await ExchangeRequestRepository(self._db_session).create_exchange_request(entity)

        return 'Ваше сообщение зарегистрировано и в скором времени мы вернемся к вам с ответом.'

