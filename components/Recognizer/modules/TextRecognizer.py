import easyocr
import numpy

from common.utils import minmax_coords_to_xywh

class TextRecognizer():
    def __init__(self):
        pass

    def read_text(self, img: numpy.ndarray):
        pass


class EasyOcrRecognizer(TextRecognizer):
    def __init__(self, allow_list):
        super().__init__()
        self.reader = easyocr.Reader(['ru', 'en'],
                                     model_storage_directory='/media/projects/ks/810-docs-parsing/components/Recognizer/recognition_model',
                                     user_network_directory='/media/projects/ks/810-docs-parsing/components/Recognizer/recognition_model',
                                     recog_network='custom_example',
                                     gpu=False)
        self.allow_list = allow_list

    @staticmethod
    def _concatenate_bboxes(bboxes):
        def points_to_minmax_coords(points):
            def get_coord(bbox, ind):
                return list(map(lambda p: p[ind], bbox))

            x_coords = get_coord(points, 0)
            y_coords = get_coord(points, 1)
            return min(y_coords), min(x_coords), max(y_coords), max(x_coords)

        points = []
        for b in bboxes:
            points.extend(b)

        y_min, x_min, y_max, x_max = points_to_minmax_coords(points)
        return x_min, y_min, x_max, y_max

    def read_text(self, img: numpy.ndarray):
        """
        recognize text from image with single line
        """
        bounds = self.reader.readtext(img,
                                 output_format='dict',
                                 mag_ratio=2,
                                 width_ths=5,
                                 allowlist=self.allow_list
                                 )

        if not bounds:
            return "", 0, []

        boxes = []
        texts = []
        confidances = []
        for b in bounds:
            # {'boxes': [[14, 9], [43, 9], [43, 22], [14, 22]],
            #   'confident': 0.2593270368261661,
            #   'text': '8ююaф'},
            boxes.append(b['boxes'])
            texts.append(b['text'])
            confidances.append(b['confident'])

        boxes_coords = minmax_coords_to_xywh(
            *self._concatenate_bboxes(boxes)
        )
        return (" ".join(texts), min(confidances), boxes_coords)
