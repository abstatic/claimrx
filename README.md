Python version: >= 3.11

Uses nanoid to generate unique id
TODO
- Cleanup the reqs file


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