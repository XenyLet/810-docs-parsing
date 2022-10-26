import time
from queue import Queue
import json

class MessageInterface:
    def __init__(self):
        pass

    @staticmethod
    def _decode_message(msg):
        return json.loads(msg)

    @staticmethod
    def _encode_message(msg):
        print("recognize 1 cell", time.time())
        return json.dumps(msg)

    def receive_message(self):
        pass

    def send_message(self, msg: dict):
        pass

class SimpleMessageInterface(MessageInterface):
    def __init__(self):
        super().__init__()
        self.receive_queue = Queue()
        self.send_queue = Queue()

    def receive_message(self):
        return self._decode_message(self.receive_queue.get())

    def send_message(self, msg: dict):
        self.send_queue.put(
            self._encode_message(msg)
        )

class ControlledMessageInterface(SimpleMessageInterface):
    def insert_msg_in_receive_queue(self, msg: dict):
        self.receive_queue.put(
            self._encode_message(msg)
        )

    def insert_msg_in_send_queue(self, msg: dict):
        self.send_queue.put(
            self._encode_message(msg)
        )

    @staticmethod
    def _observe_queue(q):
        items = q.get(block=False)

        # put them back
        for item in items[::-1]:
            q.put(item)

        return items

    def observe_receive_queue(self):
        return self._observe_queue(self.receive_queue)

    def observe_send_queie(self):
        return self._observe_queue(self.send_queue)

    def wait_for_message(self):
        return self.send_queue.get()