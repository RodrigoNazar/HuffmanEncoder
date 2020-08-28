import argparse
import pandas as pd
from pymongo import MongoClient


def main(db_name: str, csv_file: str) -> None:
    """
    Generates a csv file from a database
    :param db_name: Database with Temperature TS data
    :param csv_file: output file
    :return: None
    """
    client = MongoClient()
    db = client[db_name]
    client_sample_rate = '30T'
    table = db['temperature_t_s']
    pipeline = [{'$project': {'data': 1, '_id': 0}}, {'$unwind': '$data'},
                {'$project': {'ts': "$data.ts", 'T': "$data.val"}}]
    df = pd.DataFrame(table.aggregate(pipeline))
    df.set_index('ts', inplace=True)
    df.index = pd.to_datetime(df.index)
    df = df.resample(client_sample_rate).mean()
    df = df.diff(1).ffill().dropna()
    df.to_csv(csv_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--db_name', type=str, required=True,
                        help="mongo db with temperature")
    parser.add_argument('--csv_file', type=str, required=True,
                        help="output csv file")
    cmd_args = parser.parse_args()
    main(cmd_args.db_name, cmd_args.csv_file)
