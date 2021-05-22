# Udacity Data Streaming Nanodegree: S.F. Crime Stats project
### Q1. How did changing values on the SparkSession property parameters affect the throughput and latency of the data?
Spark is a popular framework for massive scalable data processing. Spark is optimised for volume rather than low 
latency. Changing the readStream maxOffsetsPerTrigger allows for more records to be processed but this increases 
the total latency per batch. The exact sweet spot depends on the use case we need to satisfy, as higher through put
comes at the expense of higher latency.

### Q2. What were the 2-3 most efficient SparkSession property key/value pairs? Through testing multiple variations on values, how can you tell these were the most optimal? 
There are many parameters that can be tweaked as listed here ```https://spark.apache.org/docs/latest/configuration.html```. 
The optimal combination of SparkSession property key/value pairs depends on numerous factors, namely:

* The overall architecture of the solution
* Is the solution deployed to the cloud or is it running in a local data center
* The size and type of data being processed and network latency
* Cost considerations if the solution is hosted in the cloud

Most Spark computations happen in memory, and the bottleneck are: memory, CPU and network bandwidth. The latter 
factor cannot be controlled by configuration therefore I will not cover it. 

Memory can be controlled by the following parameters:

* ```spark.driver.memory```
* ```spark.executor.memory```
* ```spark.executor.pyspark.memory```
* ```spark.python.worker.memory```


This article ```https://spark.apache.org/docs/latest/tuning.html#memory-tuning``` provides a good overview of the 
considerations to be made when optimising memory allocations. 

CPU parallelism can be controlled by the following parameters:

* ```spark.default.parallelism```
* ```maxRatePerPartition```
* ```spark.streaming.kafka.maxRatePerPartition```

CPU utilisation can be controlled by the following parameters:
* ```spark.executor.cores```
* ```spark.cores.max``` 
* ```spark.task.cpus```

Which is the most optimal set of parameters really depends on the nature of the application, data being processed, and 
the infrastructure on which it is run.

In the case of this particular project my main constrained is the terminal infrastructure made available to run the code on
and the size of the sample dataset which is quite small. There scope to perform a study on which key/value pair provides
the most optimal solution is somewhat limited, but I found that the only parameter that impacted performance was 
```spark.sql.shuffle.partitions```had the most impact on ```inputRowsPerSecond``` and ```processedRowsPerSecond``` 
which I read from the output logs. 

The table below summarises the data stats that I collected for the  ```inputRowsPerSecond``` with various 
```spark.sql.shuffle.partitions```

|Partition|min|25%|median|75%|Max|
|---|---|---|---|---|---|
|1|1.047242262|16.18705036|19.69365427|22.32142857|25.83979328|
|2|1.034245001|	14.04056162|	16.10017889|	17.37451737|	18.24817518|
|3|0.9765625|14.46945338|17.78656126|20.57613169|23.98081535|
|5|0.956937799|	12.87561576|	15.78947368|	17.40812379|	20.49180328|
|10|0.8939213349|8.83218842|10.58218979|11.55327343|	14.47178003|
|100|0.5134055904|1.82038835|2.044060868|2.184996358|	2.330398757|

The table below summarises the data stats that I collected for the ```processedRowsPerSecond``` with various 
```spark.sql.shuffle.partitions```

|Partition|min|25%|median|75%|Max|
|---|---|---|---|---|---|
|1|1.059072723|	16.04278075	|21.07728337	|23.56020942	|27.02702703|
|2|1.045174776|	18.75	|22.27722772	|24.42374254|	26.31578947|
|3|0.9864094695|	15.17706577	|18.67252066	|21.18644068|	25.38071066|
|5|0.964526846|	13.38292179	|16.00861082	|18.26206748	|22.02643172|
|10|0.9021651965|	9.086322356	|10.98901099	|11.8811933	|13.8121547|
|100|0.5162030399|	1.83939009|	2.102312544|	2.202643172|	2.340702211|

The default out-of-the-box stats without updating any parameter were:

|Parameter|min|25%|median|75%|Max|
|---|---|---|---|---|---|
|inputRowsPerSecond|0.3906080465|	1.087481875|	1.172945066|	1.197126895|	1.313887794|
|processedRowsPerSecond|0.3932019747|	1.065034645|	1.178010471|	1.201482313|	1.331380642|

Running our particular example, it appears that the highest processedRowsPerSecond was achieved with a 
spark.sql.shuffle.partitions < 5 which acheived the highest throughput.

## Running the solution
### 1. Install python dependencies
``` 
./start.sh
```

### 2. Running and Testing using the terminal console made available from Udacity

1. Run Zookeeper (mandatory for Kafka):  
```
/usr/bin/zookeeper-server-start config/zookeeper.properties
```

2. Run the Kafka server:
```
/usr/bin/kafka-server-start config/server.properties
```

3. Feed the Kafka topicvs:
```
python kafka_server.py
```  
Check the topic is correctly fed by using the kafka console consumer:
```
kafka-console-consumer --topic "org.sanfranciscopolice.calls" --from-beginning --bootstrap-server localhost:9092
```

4. Submit the Spark job:
```
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.4 --master local[*] data_stream.py
```
# Nano degree certificate
[my link](https://confirm.udacity.com/YSSDT9VA)
