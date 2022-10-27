import easyocr
import csv
from pprint import pprint
import glob

from visual_duplicates import DupFileReader

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

def _are_duplicates(ch1, ch2, dup_tuples):
    for t in dup_tuples:
        if ch1 in t and ch2 in t:
            return True
    return False

def _compare_strings(s1, s2, dup_tuples: list,
                     comparation_weakness_level=1  # the more - more loose
                     ):
    trouble_pairs = set()
    compare_result = False
    correct_letters = 0

    neg_conditions_chain = [
        lambda ch1, ch2 : ch1 != ch2,
        lambda ch1, ch2 : not _are_duplicates(ch1, ch2, dup_tuples),
        lambda ch1, ch2 : not _are_duplicates(ch1.lower(), ch2.lower(), dup_tuples),
        lambda ch1, ch2 : ch1.lower() != ch2.lower(),
        lambda ch1, ch2 : not (ch1 in (',', '.') and ch2 in (',', '.'))

    ]

    if comparation_weakness_level < 1:
        comparation_weakness_level = 1
    neg_conditions_to_apply = neg_conditions_chain[:comparation_weakness_level]

    s1 = s1.replace(" ", "")
    s2 = s2.replace(" ", "")
    if len(s1) == len(s2):
        compare_result = True
        for ch1, ch2 in zip(s1, s2):
            if all(
                    [cond(ch1, ch2) for cond in neg_conditions_to_apply]
            ):
                trouble_pairs.add((ch1, ch2))
                compare_result = False
            else:
                correct_letters+=1

    return compare_result, trouble_pairs, correct_letters



def get_duplicates(dir_w_duplicate_files):
    readers = dict()
    for f_name in glob.glob(f"{dir_w_duplicate_files}/*.duplicates"):
        readers[f_name] = DupFileReader(f_name)

    tuples = []
    for r in readers.values():
        tuples.append(set(r.duplicates_tuples))
    intersection = set.union(*tuples)

    return list(intersection)

def main(experiment_name, allow_list, test_data_dir, fonts_dir, results_dir):
    dup_tuples = get_duplicates(fonts_dir)
    trouble_pairs = set()

    print("Visual duplicates")
    pprint(dup_tuples)

    reader = easyocr.Reader(['ru', 'en'],
                            model_storage_directory='recognition_model',
                            user_network_directory='recognition_model',
                            recog_network='custom_example',
                            gpu=False)

    labels_data = []
    with open(test_data_dir + "/labels.csv", "rt") as f_labels:
        # skip header
        f_labels.readline()
        labels_data = f_labels.readlines()

    print(f"Got: {len(labels_data)} test samples")

    results = [["filename", "ground_truth", "recognized", "T-F", "confidance", "correct_letters_ratio"]]
    for l in labels_data:
        f_name, gt_text = l.replace('\n', '').split(sep=',', maxsplit=1)

        bounds = reader.readtext(test_data_dir + "/" + f_name,
                                 output_format='dict',
                                 mag_ratio=2,
                                 width_ths=5,
                                 allowlist=allow_list
                                 )

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

        boxes_coords = _concatenate_bboxes(boxes)

        gt_base = gt_text.replace(" ", "")
        rec_base = " ".join(texts).replace(" ", "")

        is_recogn_correct, new_trouble_pairs, correct_letters = _compare_strings(
            gt_base,
            rec_base,
            dup_tuples,
            comparation_weakness_level=4
        )
        trouble_pairs = trouble_pairs.union(new_trouble_pairs)

        results.append(
            [
                f_name,
                gt_base,
                rec_base,
                is_recogn_correct,
                round(min(confidances), 2),
                round(correct_letters / len(gt_base), 2)
            ]
        )

    with open(f"{results_dir}/benchmark_{experiment_name}.data.csv", "wt") as f_results:
        csv_writer = csv.writer(f_results, delimiter=',')
        csv_writer.writerows(results)

    print("\nTrouble_pairs:")
    pprint(list(trouble_pairs))

    with open(f"{results_dir}/benchmark_{experiment_name}.results.txt", "wt") as f:
        s = ''.join([''.join(p) for p in trouble_pairs])
        f.write("Trouble symbols:\n" + s + "\n")


if __name__ == '__main__':

    experiment_name = 'v6'

    allow_list = """0123456789!"%'()+,-.:;<=>?«±µ»Ω
    ABCDEFGHIJKLMNOPQRSTUVWXYZ
    abcdefghijklmnopqrstuvwxyz
    АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ
    абвгдежзиклмнопрстуфхцчшщъыьэюя"""
    test_data_dir = 'test_data'
    fonts_dir = "fonts"

    main(experiment_name, allow_list, test_data_dir, fonts_dir)
