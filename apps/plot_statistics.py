
import argparse
import matplotlib.pyplot as plt
import pandas as pd


def main(csv_file: str) -> None:
    """
    Plots the histogram and the dataframe of the data.csv
    :param csv_file: File produced by get_csv.py
    :return: None
    """
    df = pd.read_csv(csv_file, parse_dates=['ts'], index_col='ts')
    print(df.describe())
    print("numpy", df.values)

    gauss_mean, gauss_std = df['T'].mean(), df['T'].std()
    print(f"gaussian params for data mean:{gauss_mean}, std: {gauss_std}"

    df.plot(kind='hist', bins=30, density=True)
    df.plot()
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv_file', type=str, required=True,
                        help="File produced by get_csv.py")
    cmd_args = parser.parse_args()
    main(cmd_args.csv_file)
