import asyncio
import json as json_lib
import logging
from contextlib import suppress
from typing import Tuple, Optional, Any, Union, Dict

import aiohttp

from custom_exceptions import PriceServiceException
from settings import Settings

logger = logging.getLogger(__name__)


class BaseHttpService:
    _url: str = ''
    _api_key: str = ''

    async def _request(
            self, path: str, method: str = 'GET', data: Union[dict, str] = None, headers: Dict[str, str] = None,
            params: dict = None, json: dict = None, auth: aiohttp.BasicAuth = None, timeout: int = 20,
            verify_ssl=True, is_need_raw_response: bool = False
    ) -> Union[dict, bytes]:
        async with aiohttp.ClientSession() as session:

            async with session.request(
                    method=method,
                    url=''.join([self._url, path]),
                    data=data,
                    headers=headers,
                    params=params,
                    json=json,
                    auth=auth,
                    timeout=timeout,
                    verify_ssl=verify_ssl,
            ) as request:
                try:
                    if is_need_raw_response:
                        response, status_code = await self._process_response_raw(request)
                    else:
                        response, status_code = await self._process_response_json(request)
                except aiohttp.ServerTimeoutError as e:
                    logger.debug(e)
                    raise
                except aiohttp.ClientError as e:
                    logger.debug(e)

                    raise PriceServiceException
                if status_code == 500:
                    logger.error(msg='Service internal error' + str(response))
                    raise PriceServiceException

                return response

    @staticmethod
    async def _process_response_json(response: aiohttp.ClientResponse) -> Tuple[dict, int]:
        try:
            return await response.json(), response.status
        except json_lib.JSONDecodeError:
            logging.exception(
                f"Response: {(await response.content.read()).decode('utf-8')}."
            )
            raise PriceServiceException

    @staticmethod
    async def _process_response_raw(response: aiohttp.ClientResponse) -> Tuple[bytes, int]:
        return await response.content.read(), response.status

    @staticmethod
    def _process_response_exception(e: Exception) -> Tuple[Optional[Any], Optional[int]]:
        status_code = getattr(e, 'status', None)
        response_msg = getattr(e, 'message', None) or getattr(e, 'text', None)

        with suppress(json_lib.JSONDecodeError, TypeError):
            response_msg = json_lib.loads(response_msg)     # type: ignore

        return response_msg, status_code     # type: ignore


class PriceRequestService(BaseHttpService):
    def __init__(self, settings: Settings, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._url = settings.price_service_url
        self._api_key = settings.price_service_api_key

    async def _get_exchange_price(self, currency_from: str, currency_to: str) -> float:
        response = await self._request(
            path=f'/data/price',
            method='GET',
            params={
                'api_key': self._api_key,
                'fsym': currency_from,
                'tsyms': currency_to,
            }
        )
        logger.info(response)
        return response.get(currency_to.upper())

    async def get_exchange_price(self, currency_from: str, currency_to: str) -> float:
        """
         https://www.alphavantage.co/documentation/

         Получение цены за обмен

        :return: цена
        """
        return await self._get_exchange_price(currency_from, currency_to)

    @staticmethod
    async def exchange(currency_from: str, currency_to: str, amount: float) -> bool:
        await asyncio.sleep(0.2)
        return True
