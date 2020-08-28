
import argparse
import pandas as pd
import json
import os
import datetime as dt
from dahuffman import HuffmanCodec


def main(csv_file: str, enc_file: str) -> None:
    """
    Saves an instance of the Huffman codification table acording to the csv_file
    :param csv_file: File produced by get_csv.py
    :param enc_file: Path of the file to save as output
    :return: None
    """
    df = pd.read_csv(csv_file, parse_dates=['ts'])

    df['T'] = df['T'].apply(lambda x: round(x))

    unique_values = df['T'].unique()
    values = df['T']
    freq_dict = {val: (values == val).sum() for val in unique_values}

    codec = HuffmanCodec.from_frequencies(freq_dict)
    save_encoder(codec, enc_file)


def save_encoder(encoder: HuffmanCodec, enc_file: str) -> None:
    """
    Takes the encoder object and save it into the enc/ directory
    :param encoder: The encoder object
    :param enc_file: Full path of where the encoder file is going to be stored
    :param fd: First date of the samples
    :return None
    """
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # We get the encoder table
    table = encoder.get_code_table()
    # We pass it to json format
    table = {str(key): list(val) for key, val in table.items()}
    # We save the table in a json
    data = {
        'createdAt': now,
        'data': table
    }
    enc_folder = os.path.dirname(enc_file)
    if not os.path.exists(enc_folder):
        os.mkdir(enc_folder)
    with open(enc_file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv_file', type=str, required=True,
                        help="File produced by get_csv.py")
    parser.add_argument('--enc_file', type=str, default="./enc/encoder.enc",
                        help="Path of the .enc file to save as output")
    cmd_args = parser.parse_args()
    codec = main(cmd_args.csv_file, cmd_args.enc_file)
