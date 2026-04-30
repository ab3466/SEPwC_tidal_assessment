# import the modules we need
import pandas as pd
import datetime
import os
import numpy as np
import uptide
import pytz
import math
from scipy import stats
import matplotlib.dates as mdates
import argparse


def read_tidal_data(filename):
    data = pd.read_csv(filename,delim_white=True, skiprows=11,names=["date", "time", "height"])
    data["datetime"] = pd.to_datetime(data["date"] + " " + data["time"],errors="coerce")
    data["height"] = pd.to_numeric(data["height"], errors="coerce")
    data =data.dropna()

    return data
    
def extract_single_year_remove_mean(year, data):

    return 


def extract_section_remove_mean(start, end, data):

    return year_data


def join_data(data1, data2):

    return 

def sea_level_rise(data):

    return

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
    print(files)
    

if __name__ == '__main__':
    main()
