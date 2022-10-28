import numpy as np

from TextRecognizer import EasyOcrRecognizer
from multiprocessing import Queue, Process


class Worker(Process):
    def __init__(self,
                 images_queue: Queue,
                 results_queue: Queue,
                 allow_list):
        super().__init__()
        self.images_queue = images_queue
        self.results_queue = results_queue
        self.text_recognizer = EasyOcrRecognizer(allow_list)

    def _process_image(self, message) -> None:
        pass

    def run(self) -> None:
        print("Started process")
        while True:
            img = self.images_queue.get()
            print("Got image")
            res = self._process_image(img)
            print("Got result")
            self.results_queue.put(res)
            print("Sent result")


class RecognizeWorker(Worker):
    def __init__(self, images_queue: Queue, results_queue: Queue, allow_list):
        super().__init__(images_queue, results_queue, allow_list)

    def _process_image(self, image: np.ndarray) -> None:
        print("got task")
        res = self.text_recognizer.read_text(image)
        print("detected")
        return res
