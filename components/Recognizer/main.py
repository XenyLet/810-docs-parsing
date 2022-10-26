from modules.MessageInterface import ControlledMessageInterface
from modules.Worker import RecognizeWorker

if __name__ == '__main__':
    message_interface = ControlledMessageInterface()
    worker = RecognizeWorker(message_interface)
    worker.start()

    message_interface.insert_msg_in_receive_queue(
        {...}
    )
    print(message_interface.wait_for_message())

