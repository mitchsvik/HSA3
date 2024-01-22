# HSA3
Resource monitoring systems

### Structure

`docker-compose.yml` represents structure of the system. Telegraf monitoring activity in all containers.

### Project contains a web application that defines three routes:

- `GET /`: This route fetches all the timestamps from the 'timestamp' collection in the 'hsa3' database and returns them as a JSON response.

- `POST /`: This route creates a new timestamp in the 'timestamp' collection. The current date and time is added to the timestamp data and is inserted into the database. The ID of the inserted timestamp is returned in the response.

The application stores data in mongoDB and ElasticSearch

### Application testing

`siege.sh` is used to simulate load on a API by creating multiple concurrent users using the `siege` tool:
