
import argparse
import pandas as pd


def main(original_csv: str, decoded_csv: str) -> None:
    """
    Takes the two csvs files and compare them
    Made for developing the app
    :param original_csv: File produced by get_csv.py
    :param decoded_csv: File produced by decode_huff.py
    :return None
    """
    odf = pd.read_csv(original_csv, parse_dates=['ts'])
    odf['T'] = odf['T'].apply(lambda x: round(x))

    ddf = pd.read_csv(decoded_csv, parse_dates=['ts'])

    if odf.equals(ddf):
        print('THEY ARE EQUAL!')
    else:
        print('They arent equal :(')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--original_csv', type=str, required=True,
                        help="File produced by get_csv.py")
    parser.add_argument('--decoded_csv', type=str, default="./output/data.csv",
                        help="Path of the .enc file to save as output")
    cmd_args = parser.parse_args()
    main(cmd_args.original_csv, cmd_args.decoded_csv)
