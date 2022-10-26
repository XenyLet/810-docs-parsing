from .MessageInterface import MessageInterface
from .TextRecognizer import TextRecognizer
import threading
from .pdf_processing import run as img_processor


class Worker(threading.Thread):
    def __init__(self, message_interface: MessageInterface,
                 text_recognizer: TextRecognizer):
        super().__init__()
        self.message_interface = message_interface
        self.text_recognizer = text_recognizer

    def _process_message(self, message) -> None:
        pass

    def run(self) -> None:
        while True:
            new_message = self.message_interface.receive_message()
            self._process_message(new_message)


class RecognizeWorker(Worker):
    def __init__(self, 
                 message_interface: MessageInterface, 
                 text_recognizer: TextRecognizer):
        super().__init__(message_interface, text_recognizer)

    def _process_message(self, message: dict) -> None:
        """
        Processes messages like 
        {
	        task_id:   57092,
	        file_name: "/data/reports/docs/ИБПА.325321.СВЫ666.pdf"
        }
        """
        recognition_results = img_processor.run(
            message["file_name"],
            self.text_recognizer
        )
        result = {
            "status": "temp",
            "message": "test message",
            "task_id": message["task_id"],
            "data":{
                "recognition_results": recognition_results
            }
        }
        self.message_interface.send_message(result)
