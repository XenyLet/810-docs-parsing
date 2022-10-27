import os

import benchmark, benchmark_results_review

full_path =os.path.realpath(__file__)
PWD = os.path.dirname(full_path)
MODEL_ZOO_DIR="recognition_model/model_zoo"
CURRENT_MODEL="recognition_model/custom_example.pth"

def relink_model(new_experiment_name):
    os.unlink(CURRENT_MODEL)
    os.symlink(
        os.path.join(PWD,
                     MODEL_ZOO_DIR,
                     f"ru_filtered_{new_experiment_name}",
                     "best_accuracy.pth"),
        os.path.join(PWD,
                     CURRENT_MODEL)
    )

def main(experiment_name, allow_list, test_data_dir, fonts_dir,results_dir):
    relink_model(experiment_name)
    benchmark.main(experiment_name, allow_list, test_data_dir, fonts_dir, results_dir)
    benchmark_results_review.main(experiment_name, results_dir)

if __name__ == '__main__':
    allow_list = """0123456789!"%'()+,-.:;<=>?«±µ»Ω
        ABCDEFGHIJKLMNOPQRSTUVWXYZ
        abcdefghijklmnopqrstuvwxyz
        АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ
        абвгдежзиклмнопрстуфхцчшщъыьэюя"""
    test_data_dir = 'test_data'
    fonts_dir = "fonts"
    results_dir = "results"

    for n in ["6"]:
        experiment_name = f'v{n}'
        main(experiment_name, allow_list, test_data_dir, fonts_dir,results_dir)