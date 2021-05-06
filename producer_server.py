from kafka import KafkaProducer
import json
import time


class ProducerServer(KafkaProducer):
    print("Running producer server")

    def __init__(self, input_file, topic, **kwargs):
        super().__init__(**kwargs)
        self.input_file = input_file
        self.topic = topic

    # generating a dummy data
    def generate_data(self):
        with open(self.input_file) as f:
            data = json.load(f)
            for line in data:
                message = self.dict_to_binary(line)
                # send the correct data
                self.send(self.topic, message)
                time.sleep(1)

    # fill this in to return the json dictionary to binary
    @staticmethod
    def dict_to_binary(json_dict):
        return json.dumps(json_dict).encode('utf-8')
