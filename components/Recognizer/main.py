import time

from modules.MessageInterface import ControlledMessageInterface
from modules.Worker import RecognizeWorker
from modules.TextRecognizer import EasyOcrRecognizer

if __name__ == '__main__':
    message_interface = ControlledMessageInterface()
    text_recognizer = EasyOcrRecognizer(allow_list="""0123456789!"%'()+,-.:;<=>?«±µ»Ω
ABCDEFGHIJKLMNOPQRSTUVWXYZ
abcdefghijklmnopqrstuvwxyz
АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ
абвгдежзиклмнопрстуфхцчшщъыьэюя""")
    worker = RecognizeWorker(message_interface,
                             text_recognizer)
    worker.start()
    print (time.time())
    message_interface.insert_msg_in_receive_queue(
        {
            "task_id": 1,
            "file_name": "/media/projects/ks/810-docs-parsing/src_pdf/ИБПА.468163.021ПЭ3.pdf"
        }
    )
    print(message_interface.wait_for_message())

