# import the modules we need
import pandas as pd
import datetime
import os
import numpy as np
# import uptide
# import pytz
import math
from scipy import stats
import matplotlib.dates as mdates
import argparse


def read_tidal_data(filename):

    data = pd.read_csv(
        filename,
        sep=r"\s+",
        skiprows=11,
        names=["date", "time", "height", "residuals"])

    data["datetime"] = pd.to_datetime(
        data["date"] + " " + data["time"],
        format="%Y/%m/%d %H:%M:%S",
        errors="coerce")

    data["height"] = pd.to_numeric(
        data["height"],
        errors="coerce")

    print(data.head())

    return data
    
def extract_single_year_remove_mean(year, data):

    year_data = data[data["datetime"].dt.year == year]

    mean_height = year_data["height"].mean()

    year_data["residuals"] = year_data["height"] - mean_height

    print(year_data.head())

    return year_data 


def extract_section_remove_mean(start, end, data):

    print(data["datetime"].min(), data["datetime"].max())
    
    section_data = data[
    (data["datetime"] >= start) &
    (data["datetime"] <= end)].copy()

    mean_height = section_data["height"].mean()

    section_data["residuals"] = (
        section_data["height"] - mean_height)

    print(section_data.head())

    return section_data


def join_data(data1, data2):

    combined_data = pd.concat([data1, data2])

    combined_data = combined_data.sort_values(by="datetime")

    print(combined_data.head())

    return combined_data

def sea_level_rise(data):

    yearly_mean = data.groupby(
        data["datetime"].dt.year)["height"].mean()

    print(yearly_mean)

    return yearly_mean

def tidal_analysis(data, constituents, start_datetime):

    return

def get_longest_contiguous_data(data):

    return 


def main(args_list=None):

    parser = argparse.ArgumentParser(
                     prog="UK Tidal analysis",
                     description="Calculate tidal constiuents and RSL from tide gauge data",
                     )

    parser.add_argument("directory",
                    help="the directory containing txt files with data")
    parser.add_argument('-v', '--verbose',
                    action='store_true',
                    default=False,
                    help="Print progress")

    args = parser.parse_args(args_list)
    dirname = args.directory
    verbose = args.verbose

    files = os.listdir(dirname)
    
    txt_files = []
    
    for file in files:
        if file.endswith(".txt"):
            txt_files.append(file)
    
        
    for file in txt_files:

     filepath = os.path.join(dirname, file)

     data = read_tidal_data(filepath)

     year_data = extract_single_year_remove_mean(2018, data)

     section_data = extract_section_remove_mean(
        pd.Timestamp("2019-01-01"),
        pd.Timestamp("2019-01-31 23:59:59"),
        data)

     combined = join_data(year_data, section_data)

    print(combined.head())
    slr = sea_level_rise(data)

    print(slr)

if __name__ == '__main__':
    main()
