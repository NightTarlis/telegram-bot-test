from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class UserRequestStatusEnum(str, Enum):
    created = 'created'
    failed = 'failed'
    finished = 'finished'
    need_moderation = 'need_moderation'


class User(BaseModel):
    id: Optional[int] = Field(None)
    external_id: Optional[int] = Field(0)
    username: Optional[str] = Field('')
    fullname: Optional[str] = Field('')


class ExchangeRequest(BaseModel):
    id: Optional[int] = Field(0)
    msg_id: Optional[int] = Field(0)
    external_user_id: Optional[int] = Field(0)
    chat_id: Optional[int] = Field(0)
    status: UserRequestStatusEnum = UserRequestStatusEnum.created.value
    msg_text: Optional[str] = Field('')
    currency_from: Optional[str] = Field('')
    currency_to: Optional[str] = Field('')
    amount: Optional[float] = Field(0)
    price: Optional[float] = Field(0)
    created_at: Optional[datetime] = Field(datetime.utcnow())
    updated_at: Optional[datetime] = Field(datetime.utcnow())


class UserBalance(BaseModel):
    id: Optional[int] = Field(None)
    external_user_id: Optional[int] = Field(0)
    currency: Optional[str] = Field('')
    amount: Optional[float] = Field(0.0)


class Currency(BaseModel):
    id: Optional[str] = Field(None)
    symbol: Optional[str] = Field('')
    name: Optional[str] = Field('')
