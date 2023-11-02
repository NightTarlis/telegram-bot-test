from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_name: str = 'tg-bot-test-task'

    tg_bot_token: str = Field('6765574486:AAGaltce0m0KMM4VqXC-mDg6bVuSwjVE5lk', env='TG_BOT_TOKEN')

    price_service_url: str = Field('https://min-api.cryptocompare.com', env='PRICE_SERVICE_URL')
    price_service_api_key: str = Field(
        '5844106d798f2ca7c95727dff36e86c9c8f5730f00d2b37e3d72808ee076262b', env='PRICE_SERVICE_API_KEY'
    )

    db_host: str = Field('postgres-bot', env='DB_HOST')
    db_port: int = Field(5432, env='DB_PORT')
    db_user: str = Field('postgres', env='DB_USER')
    db_password: str = Field(None, env='DB_PASSWORD')
    db_name: str = Field('postgres', env='DB_NAME')
    db_data: str = Field('/var/lib/postgresql/data/pgdata', env='DB_DATA')

    model_config = SettingsConfigDict(
        # `.env.prod` takes priority over `.env`
        env_file=('.env', '.env.prod'),
        extra='forbid'
    )