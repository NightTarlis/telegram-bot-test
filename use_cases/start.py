from adapters.repositories.user import UserRepository
from adapters.repositories.user_balances import UserBalanceRepository
from entities.dto import UserDTO
from entities.entities import User, UserBalance
from settings import Settings
from use_cases import BaseInteractor

settings = Settings()


class StartInteractor(BaseInteractor):
    async def execute(self, user: UserDTO) -> str:

        user_exist = await UserRepository(self._db_session).check_user_exists(User(external_id=user.id))
        if user_exist:
            reply_text = f'''```
        Здравствуйте, {user.first_name}!
        Это бот для коммуникации c некоторой компанией по вопросам покупки/продажи валют.

        Доступные команды:
        • Для покупки или продажи валюты используйте формат:
          - buy 100 BTC/USDT - для покупки 100 BTC за USDT
          - sell 0.3 Eth/BTC - для продажи 0.3 ETH и получения соответствующего количества BTC

        • report - для вывода PNL и позиций по каждому активу

        Если у вас есть другие вопросы или сообщение, напишите их сюда и представитель компании свяжется с вами.
                   ```'''
        else:
            await UserRepository(self._db_session).create_user(
                User(external_id=user.id, username=user.username, fullname=user.full_name)
            )
            await UserBalanceRepository(self._db_session).create_base_balance(
                UserBalance(external_user_id=user.id, currency='usdt', amount=10000.0)
            )

            reply_text = f'''```
        Здравствуйте, {user.first_name}!
        Это бот для коммуникации c некоторой компанией по вопросам покупки/продажи валют.
        По умолчанию у каждого клиента есть баланс 10000 usdt.

        Доступные команды:
        • Для покупки или продажи валюты используйте формат:
          - buy 100 BTC/USDT - для покупки 100 BTC за USDT
          - sell 0.3 Eth/BTC - для продажи 0.3 ETH и получения соответствующего количества BTC

        • report - для вывода PNL и позиций по каждому активу

        Если у вас есть другие вопросы или сообщение, напишите их сюда и представитель компании свяжется с вами.
                   ```'''

        return reply_text
