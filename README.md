# Users

Service for telegram bot.
 
## Testing
* Run unit tests - `pytest tests/unit`
* Run cases (flow/integration) tests - `pytest tests/cases`
* Run single test - `pytest tests/path/to/test_some.py`


## Running
Прописать в файл .env переменные окружения (зарегистрировать бота для телеграма)
* docker-compose build
* docker-compose up -d 
ИЛИ поднять отдельно инстанс постгреса и 
* poetry install
* poetry run python migration.py
* poetry run python main.py


## DATABASE
- DB_HOST - database host
- DB_PORT - database port
- DB_USER - database username
- DB_PASSWORD - database password
- DB_NAME - database name
- DB_DATA - path for postgres data


## APP envs
- TG_BOT_TOKEN - telegram bot token
- PRICE_SERVICE_URL - api for price service
- PRICE_SERVICE_API_KEY - api key for price service
