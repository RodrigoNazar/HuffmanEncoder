
import argparse
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta
from dahuffman import HuffmanCodec


EOF = list(HuffmanCodec.from_frequencies({0: 1}).get_code_table().keys())[0]


def main(csv_file: str, enc_file: str, huff_file: str) -> None:
    """
    Decodes the entire .huff file into a .csv file
    :param csv_file: Path of the csv file to save
    :param enc_file: File produced by create_encoder.py (.enc)
    :param huff_file: Path of the .huff compressed csv
    :return: None
    """
    with open(huff_file, 'rb') as f:
        file = f.read()
        metadata = file[:57]
        data = file[57:]

    # Unpacking the metadata
    metadata = metadata.decode('UTF-8')
    createdAt, first_ts, _ = metadata.split('\n')
    createdAt = createdAt.split('createdAt')[1]
    first_ts = first_ts.split('first_ts')[1]

    # Get de decoder
    codec, _ = get_encoder(enc_file)

    ts = datetime.strptime(first_ts, "%Y-%m-%d %H:%M:%S")

    Tdf = pd.DataFrame(codec.decode(data), columns=['T'])
    df = pd.DataFrame({
        'ts': [ts + i*timedelta(minutes=30) for i in range(len(Tdf))],
        'T': codec.decode(data)
    })
    df.set_index('ts', inplace=True)

    csv_folder = os.path.dirname(csv_file)
    if not os.path.exists(csv_folder):
        os.mkdir(csv_folder)

    df.to_csv(csv_file)


def get_encoder(enc_file):
    """
    Takes the path of the .enc load the instance of the encoder
    :param enc_file: Path of the .enc file
    :return None
    """
    with open(enc_file) as json_file:
        enc_file = json.load(json_file)
        data = enc_file['data']
        createdAt = enc_file['createdAt']
        new_data = {}
        for key, val in data.items():
            if key != '_EOF':
                new_data[np.int64(key)] = tuple(val)
            else:
                new_data[EOF] = tuple(val)
        return HuffmanCodec(new_data, check=False), createdAt


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv_file', type=str, required=True,
                        help="Path of the csv file to save")
    parser.add_argument('--enc_file', type=str,
                        default="./enc/encoder.enc",
                        help="File produced by create_encoder.py")
    parser.add_argument('--huff_file', type=str,
                        default="./output/data.huff",
                        help="Path of the .huff compressed csv")
    cmd_args = parser.parse_args()
    codec = main(cmd_args.csv_file, cmd_args.enc_file,
                 cmd_args.huff_file)
