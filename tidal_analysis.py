# import the modules we need
import pandas as pd
import os
import argparse
from scipy import stats
import warnings
import datetime

# Reads tidal data from a text file and formats datetime values
def read_tidal_data(filename):

    data = pd.read_csv(
        filename,
        sep=r"\s+",
        skiprows=11,
        names=["Date", "Time", "Sea Level", "Residual"])

    data["datetime"] = pd.to_datetime(
        data["Date"] + " " + data["Time"],
        format="%Y/%m/%d %H:%M:%S",
        errors="coerce")

    data["Sea Level"] = pd.to_numeric(
        data["Sea Level"],
        errors="coerce")
    
    data["Residual"] = pd.to_numeric(
        data["Residual"],
        errors="coerce")

    data.set_index("datetime", inplace=True)

    return data
    
# Extracts data from a selected year and removes the mean sea level
def extract_single_year_remove_mean(year, data):

    year_data = data[data.index.year == int(year)].copy()

    mean_height = year_data["Sea Level"].mean()

    year_data["Sea Level"] = year_data["Sea Level"] - mean_height

    return year_data 

# Extracts a time section of data and removes the mean sea level
def extract_section_remove_mean(start, end, data):
    
    section_data = data.loc[start:end].copy()

    mean_height = section_data["Sea Level"].mean()

    section_data["Sea Level"] = (
        section_data["Sea Level"] - mean_height)


    return section_data

# Combines two datasets and sorts them by datetime
def join_data(data1, data2):

    combined_data = pd.concat([data1, data2])

    combined_data = combined_data.sort_index()


    return combined_data

# Calculates sea level rise statistics using linear regression
def sea_level_rise(data):

    yearly_mean = data.groupby(
        data.index.year)["Sea Level"].mean()

    years = yearly_mean.index
    sea_levels = yearly_mean.values

    if len(years) < 2:
        return float("nan"), float("nan")

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        slope, intercept, r_value, p_value, std_err = (
            stats.linregress(years, sea_levels)
        )

    return slope, p_value

# Performs tidal constituent analysis and summarises residual data
def tidal_analysis(data, constituents, start_datetime):

    residual_mean = data["Residual"].mean()

    return constituents, residual_mean

# Finds the longest continuous block of tidal data
def get_longest_contiguous_data(data):

    data = data.sort_index()

    time_diff = data.index.to_series().diff()

    gap_mask = time_diff > pd.Timedelta(minutes=15)

    group_id = gap_mask.cumsum()

    groups = data.groupby(group_id)

    longest_group = max(groups, key=lambda x: len(x[1]))[1]


    return longest_group

# Main function for loading, processing and analysing tidal datasets
def main(args_list=None):

    parser = argparse.ArgumentParser(
        prog="UK Tidal analysis",
        description=(
            "Calculate tidal constiuents and RSL "
            "from tide gauge data"
        ),
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

        if verbose:
            print(f"Processing {file}")

        filepath = os.path.join(dirname, file)

        data = read_tidal_data(filepath)

        year_data = extract_single_year_remove_mean(2018, data)

        section_data = extract_section_remove_mean(
            pd.Timestamp("2019-01-01"),
            pd.Timestamp("2019-01-31 23:59:59"),
            data)

        combined = join_data(year_data, section_data)
        
        # Calculate sea level rise statistics
        slr = sea_level_rise(data)
        slope, p_value = slr
        
        if verbose:
            # print(f"Sea level rise slope: {slope}")
            # print(f"P-value: {p_value}")
            print("-" * 40)
        # Identify the longest continuous section of valid data
        longest_data = get_longest_contiguous_data(data)

        if verbose:
            print(longest_data.head())
         

if __name__ == '__main__':
    main()
