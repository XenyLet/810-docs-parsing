import pandas as pd
from pprint import pprint, pformat

def get_col(row, col_num):
    return row[col_num]

def main(experiment_name, results_dir):
    results = pd.read_csv(f"{results_dir}/benchmark_{experiment_name}.data.csv")

    # remove header
    stats = {
        "conf (med, std)": (results["confidance"].median(), round(results["confidance"].std(), 2)),
        "T_str_ratio": round(results["T-F"].mean(), 2),
        "correct_letters_ratio (med, std)": (results["correct_letters_ratio"].median(), round(results["correct_letters_ratio"].std(), 2)),
    }

    print("\nStatistics:")
    pprint(stats)

    with open(f"{results_dir}/benchmark_{experiment_name}.results.txt", "at") as f:
        s = "\n\nStatistics:\n"
        f.write(s)
        s = pformat(stats)
        f.write(s)

    print("correlations:")
    results_corr = results.corr()
    print(results_corr)
    with open(f"{results_dir}/benchmark_{experiment_name}.results.txt", "at") as f:
        s = "\n\nCorrelations:\n"
        f.write(s)
        s = pformat(results_corr)
        f.write(s)


if __name__ == '__main__':
    main(experiment_name = "v6", results_dir="results")

