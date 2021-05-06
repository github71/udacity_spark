
### Install python dependencies
``` 
./start.sh
```

## Running and Testing using the terminal console made available from Udacity
1. Run Zookeeper (mandatory for Kafka):  
`/usr/bin/zookeeper-server-start config/zookeeper.properties`
2. Run the Kafka server:  
`/usr/bin/kafka-server-start config/server.properties`
3. Feed the Kafka topics:  
`python kafka_server.py`  
Check the topic is correctly fed by using the kafka console consumer:  
`kafka-console-consumer --topic "org.sanfranciscopolice.calls" --from-beginning --bootstrap-server localhost:9092`
4. Submit the Spark job:  
`spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.4 --master local[*] data_stream.py`