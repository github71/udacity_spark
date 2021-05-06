import producer_server

topic = "org.sanfranciscopolice.calls"
bootsrap_server = "localhost:9092"


def run_kafka_server():
    # get the json file path
    input_file = "police-department-calls-for-service.json"

    # fill in blanks
    print(f"Producing topic {topic}")
    producer = producer_server.ProducerServer(
        input_file=input_file,
        topic=topic,
        bootstrap_servers=bootsrap_server,
        client_id="producer",
        api_version=(0, 10, 1)
    )

    return producer


def feed():
    producer = run_kafka_server()
    producer.generate_data()


if __name__ == "__main__":
    feed()
