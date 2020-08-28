'''
Util:
from bitstring import BitArray

c = BitArray(hex=codec.encode([0, 1, 8]).hex())
print(c.bin)
'''
import argparse
import pandas as pd
import numpy as np
import json
import os
from dahuffman import HuffmanCodec
import datetime as dt


EOF = list(HuffmanCodec.from_frequencies({0: 1}).get_code_table().keys())[0]


def main(csv_file: str, enc_file: str, huff_file: str) -> None:
    """
    Encondes the entire csv file into a .huff file
    :param csv_file: File produced by get_csv.py
    :param enc_file: File produced by create_encoder.py (.enc)
    :param huff_file: Path of the .huff compressed csv
    :return: None
    """
    codec = get_encoder(enc_file)
    df = pd.read_csv(csv_file, parse_dates=['ts'])
    df['T'] = df['T'].apply(lambda x: round(x))

    first_ts = df['ts'][0].strftime("%Y-%m-%d %H:%M:%S")
    createdAt = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    huff_folder = os.path.dirname(huff_file)
    if not os.path.exists(huff_folder):
        os.mkdir(huff_folder)

    with open(huff_file, 'wb') as f:
        f.write('createdAt'.encode('UTF-8'))
        f.write(createdAt.encode('UTF-8'))
        f.write('\n'.encode('UTF-8'))
        f.write('first_ts'.encode('UTF-8'))
        f.write(first_ts.encode('UTF-8'))
        f.write('\n'.encode('UTF-8'))
        f.write(codec.encode(df['T']))


def get_encoder(enc_file):
    """
    Takes the path of the .enc load the instance of the encoder
    :param enc_file: Path of the .enc file
    :return None
    """
    with open(enc_file) as json_file:
        enc_file = json.load(json_file)
        data = enc_file['data']
        new_data = {}
        for key, val in data.items():
            if key != '_EOF':
                new_data[np.int64(key)] = tuple(val)
            else:
                new_data[EOF] = tuple(val)
        return HuffmanCodec(new_data, check=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv_file', type=str, required=True,
                        help="File produced by get_csv.py")
    parser.add_argument('--enc_file', type=str,
                        default="./enc/encoder.enc",
                        help="File produced by create_encoder.py")
    parser.add_argument('--huff_file', type=str,
                        default="./output/data.huff",
                        help="Path of the .huff compressed csv")
    cmd_args = parser.parse_args()
    codec = main(cmd_args.csv_file, cmd_args.enc_file,
                 cmd_args.huff_file)
