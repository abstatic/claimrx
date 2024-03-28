
Python version: >= 3.11

## Local Development

API gets hosted on `localhost:8000`

1. Bootstrap the machine using `bash bootstrap.sh` script
2. Local development server can be started using `bash develop_local.sh [runserver|test|docker]` for running local server or tests or docker
   1. `bash develop_local.sh docker` would only make single container
   2. `bash develop_local.sh dockercompose` would run with postgresql support using docker compose. To kill docker compose use docker-compose down

#### Features
- unique id using nanoid
- Ratelimiting using slowapi
- middleware example
- aggregation and grouping at database level
- support for both sqlite3 and postgresql. refer `db.py` to change the connection string
- logic for validation and easy to extend validation
- logic for input parameter disambugation: lowercase and repalce spaces with single underscore (snake_case)

### What could be better:
- Exception handling
- Error messaging
- Validation error handling, have legible error messaging
- Logging, logging to a file, logging inside docker container, shipping logs
- No DB migration manager
- Async database sessions

#### How claim_process will communicate with payments, Propose a reasonable solution based on:
 - What needs to be done if there is a failure in either service and steps need to be unwinded.
 - Multiple instances of either service are running concurrently to handle a large volume of claims.

**Answer** :
Scenario: If `payment_service` is to be treated as a downstream service and the `claim_service` should notify 
`payment service` 

Both the services need to be stateless. The backing data stores should be managed and have HA and replicas.
For a resilient architecture we should use some sort of message broking b/w these two components
This can be easily implemented using Kafka. If kafka feels like a overkill a HA key-value store like redis can also suffice
we just need to keep a track of how many claims have been generated and how many has the payment_service consumed.

For handling concurrency there could be multiple options:
 - Introduce atomicity for the operation
 - Have fixed number of instances of payment_service and have them subscribed to partitions on kafka
 - Use counting semaphores to dynamically create a threadpool of a fixed size which can grow and shrink as per demand.

In the case it so happens that the backing data stores are lost/corrupted OR we want to undo operation:
- To mitigate this we need backup policies - take regular snapshots of data and put them into long term storage
- For the delta of time above, log based operations can be applied. (Use write ahead log)
- In the log files we keep track of every claim that was inserted / received.

Log Format:
- If we want any sort of log based recovery / analysis then log messages while insertion should be structured as such.