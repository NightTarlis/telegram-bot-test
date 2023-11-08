from typing import Optional

from pydantic import BaseModel, Field


class MessageDTO(BaseModel):
    id: Optional[int] = Field(0)
    external_user_id: Optional[int] = Field(0)
    chat_id: Optional[int] = Field(0)
    text: Optional[str] = Field('')


class UserDTO(BaseModel):
    id: Optional[int] = Field(0)
    first_name: Optional[str] = Field('')
    username: Optional[str] = Field('')
    full_name: Optional[str] = Field('')
