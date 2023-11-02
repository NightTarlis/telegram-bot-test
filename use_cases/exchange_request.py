import datetime
import logging

from telegram import Message

from adapters.repositories import ExchangeRequestRepository, UserBalanceRepository, CurrencyRepository
from adapters.services import PriceRequestService
from custom_exceptions import PriceServiceException
from entities.entities import ExchangeRequest, UserRequestStatusEnum, UserBalance
from settings import Settings
from use_cases import BaseInteractor

settings = Settings()

logger = logging.getLogger(__name__)


class ExchangeRequestInteractor(BaseInteractor):

    async def execute(self, message: Message, external_user_id: int) -> str:
        operation, amount_from, currency_from, currency_to = await ExchangeRequestRepository.parse_message(
            message.text
        )

        if operation == 'buy':
            currency_from, currency_to = currency_to, currency_from

        if currency_from and currency_to:
            currency_from = await CurrencyRepository.normalize_to_symbol(currency_from)
            currency_to = await CurrencyRepository.normalize_to_symbol(currency_to)

        now = datetime.datetime.utcnow()

        entity = ExchangeRequest(
            msg_id=message.id,
            external_user_id=external_user_id,
            chat_id=message.chat_id,
            status=UserRequestStatusEnum.finished.value,
            msg_text=message.text,
            currency_from=currency_from,
            currency_to=currency_to,
            amount=amount_from,
            created_at=now,
            updated_at=now
        )

        if not currency_from or not currency_to:
            entity.status = UserRequestStatusEnum.need_moderation.value
            await ExchangeRequestRepository(self._db_session).create_exchange_request(entity)
            return 'Извините, мы не смогли разобрать ваше обращение. ' \
                'Менеджер нашей компании скоро свяжется с вами для уточнения заявки.'

        try:
            price = await PriceRequestService(settings).get_exchange_price(currency_to, currency_from)
            if not price:
                raise PriceServiceException
        except PriceServiceException:
            entity.status = UserRequestStatusEnum.failed.value
            await ExchangeRequestRepository(self._db_session).create_exchange_request(entity)
            return 'Извините, сервис для получения цен временно не работает'

        if operation == 'buy':
            amount_to = amount_from * price
        else:
            amount_to = amount_from * 100_000 / price / 100_000

        entity.price = amount_to

        result = f'Сделка по обмену {currency_from} на {currency_to} состоялась, по цене {amount_to}'

        if not await UserBalanceRepository(self._db_session).check_can_user_exchange_currency(
                UserBalance(external_user_id=external_user_id, currency=currency_from, amount=amount_from)
        ):
            entity.status = UserRequestStatusEnum.failed.value
            result = 'Сделка не состоялась - на балансе недостаточно средств'

        if not await PriceRequestService(settings).exchange(currency_from, currency_to, amount_from):
            entity.status = UserRequestStatusEnum.failed.value
            result = 'Сделка не состоялась - сервис обмена не работает'

        await ExchangeRequestRepository(self._db_session).create_exchange_request(entity)

        if entity.status == UserRequestStatusEnum.finished.value:
            if operation == 'buy':
                amount_from, amount_to = amount_to, amount_from

            await UserBalanceRepository(self._db_session).update_user_balance(
                UserBalance(external_user_id=external_user_id, currency=currency_from, amount=-amount_from)
            )
            await UserBalanceRepository(self._db_session).update_user_balance(
                UserBalance(external_user_id=external_user_id, currency=currency_to, amount=amount_to)
            )

        return result
