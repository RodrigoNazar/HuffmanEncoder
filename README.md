
# HuffmanEncoder

A set of apps that get the temperature data from a csv file and generate the Huffman codification of that set.

## Features

* ```get_csv.py:``` Generates a csv file from the database.
* ```plot_statistics.py:``` Plots the histogram and the dataframe of the data.csv.
* ```create_encoder.py:``` Saves an instance of the Huffman codification table acording to the csv_file.
* ```encode_csv.py:``` Encondes the entire csv file into a .huff file.
* ```decode_huff.py:``` Decodes the .huff file encoded with ```encode_csv.py``` into a .csv file.
* ```compare_csvs.py:``` Compares the cvs's files gotten by executing the ```get_csv.py:``` and ```decode_huff.py``` apps.

## Usage

The main usage of the feature is to generate the csv file from the database running the ```get_csv.py``` app with the database name.

Then run the ```create_encoder.py``` referencing the .csv file that is going to be compressed. There, the .enc file will be generated

Now run the ```encode_csv.py``` app, referencing the .enc file and the .huff file will be created from the .csv file.

If you want to decode the .huff file, run the ```decode_huff.py``` app with the .enc file path and the .csv will be created.


#### CSV file format

The format of the csv file needs to be like following:

```data.csv```

| ts        | T           |
| :-------------: |:-------------:|
| 2019-11-22 16:00:00   | 0.43404873686564116 |
| 2019-11-22 16:30:00   | 0.8711155823831866  |
| ... | ...      |

Using a ',' as separator and '.' as the caracter to recognize as decimal point.

## To do

* develop a ```get_huff.py```, that creates the .huff file directly from the DB instead of a .csv file.

* develop the following enpoints handlers to operate the apps:
  - get_encoder: to import (via scp (?)) an specific version of the encoders (acording to the date, or the month).
  - create_encoder: to create an specific .enc acording to a specific date range.
  - get_huff: to import (via scp (?)) an specific .huff acording to a specific date range.
