# SoftwareEngineerTestCase


## Installation
```bash
1. install docker && docker-compose
2. cp .env.example .env # and fill it
```

## Usage
```bash
1. docker-compose up --build --d
```

## Description
1. You can find answers to task 1.1 points 1-4 in the /answers folder or inside the docker container in the /answers folder
2. You can find SQL queries for task 1.1 are in the following paths:
   - Taks 1.1.1 /tasks/event/get_percent_by_last_40_t_for_symbol.py
   - Taks 1.1.2 /tasks/event/calculate_the_average_dollar_volume.py
   - Taks 1.1.3 /tasks/event/rank_stocks_by_positive_volume.py
   - Taks 1.1.4 /tasks/event/calculate_average_absolute_daily_percent_change.py
3. To connect to websocket via postman use link ```ws://<YOUR_SERVER_IP>:<WEBSOCKET_PORT_FROM_ENV>```
4. For check websocket test logs ```docker logs <WEBSOCKET_TEST_CONTAINER_ID>```
## License

[MIT](https://choosealicense.com/licenses/mit/)
