"""Question 5"""
import os
import pandas as pd
from zipfile import ZipFile

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
FILE_DIR = os.path.join(ROOT_DIR, 'data')
FILE_PATH = os.path.join(FILE_DIR, 'data.csv')


class WeatherAnalysisSolution:

    def __init__(self):
        self.weather_data = None

    def find_lowest_temp_station_date(self):
        """
        Part 1 - Finds the station id and date of the lowest temperature. If there is more than one instance
        of the lowest temperature return one at random.
        :returns: station_id, date combo for the row with the lowest temperature
        """
        # get the min of the temperature_c field and filter to all instances when min occurred
        min_temp_data = self.weather_data[self.weather_data.temperature_c == self.weather_data.temperature_c.min()]
        # choose a random sample from those that match the criteria
        min_random_sample = min_temp_data.sample().iloc[0]
        min_station_id = min_random_sample.station_id
        min_date = min_random_sample.date

        return int(min_station_id), float("{:.3f}".format(min_date))

    def find_station_with_most_fluctuation(self):
        """Part 2 - Finds the station with the most temperature fluctuation, returns the station ID"""
        station_ids = self.get_weather_station_ids(self.weather_data)  # get a list of all the weather station IDs
        # make a dictionary of station_id and amount of fluctuation pairs
        flux_by_station = {station_id: self.calc_station_fluctuation(station_id)
                           for station_id in station_ids}
        # return the station_id key of the max value in the dict
        max_flux_station = max(flux_by_station, key=flux_by_station.get)

        return int(max_flux_station)

    def find_station_with_most_fluctuation_date_range(self, start_date, end_date):
        """Part 3 - Finds the station with the most temperature fluctuation during a given date range and
        returns the station ID"""
        # would check input validity here i.e:
        # if not self.is_valid_date(start_date) or not self.is_valid_date(end_date):
        #     raise ValueError("Please enter two valid dates")

        station_ids = self.get_weather_station_ids(self.weather_data)  # get a list of all the weather station IDs
        # make a dictionary of station_id and amount of fluctuation pairs
        flux_by_station = {station_id: self.calc_station_fluctuation_date_range(station_id, start_date, end_date)
                           for station_id in station_ids}
        # should make sure to handle the case of no max
        max_flux_station = max(flux_by_station, key=flux_by_station.get)

        return int(max_flux_station)  # return the station_id key of the max value in the dict

    def calc_station_fluctuation(self, station_id):
        """Finds the amount of fluctuation between each day at a weather given station and returns the total"""
        station_data = self.filter_data_by_station(self.weather_data, station_id)

        return self.calc_temp_fluctuation(station_data)  # calculate fluctuation

    def calc_station_fluctuation_date_range(self, station_id, start_date, end_date):
        """Find the fluctuation at one station for a given date range"""
        station_data = self.filter_data_by_station(self.weather_data, station_id)  # get station data
        # filter by date range
        station_data_for_dates = self.filter_station_data_by_date_range(station_data, start_date, end_date)

        # calculate fluctuation, if station_data_for_dates is empty df return -1
        return self.calc_temp_fluctuation(station_data_for_dates) if not station_data_for_dates.empty else -1

    @staticmethod
    def calc_temp_fluctuation(df):
        """Finds the amount of temperature fluctuation between each day and returns the total"""
        temp_diff = df.temperature_c.diff()  # get the difference between one temperature and the last
        temp_diff_abs = temp_diff.abs()  # find the absolute value of all the differences

        return temp_diff_abs.sum()  # sum up all the absolute values to get the fluctuation

    @staticmethod
    def filter_data_by_station(df, station_id):
        """Filters a pandas dataframe down to a particular station"""
        return df[df.station_id == station_id]

    def filter_station_data_by_date_range(self, df, start_date, end_date):
        """Filters a data frame down to a particular date range -- this should be used when station data is
        already filtered"""

        if not len(self.get_weather_station_ids(df)) == 1:
            raise ValueError("please filter this dataframe to one station")

        # I'm assuming that the data is in order here, and that we want to use a station only if it has a full data set
        # for the range. I would have changed this to pull any available data before the end date cutoff
        # if we can assume 2000.001 is before 2000.002
        start_indices = df[df.date == start_date].index.values.astype(int)  # get the index of the start date
        end_indices = df[df.date == end_date].index.values.astype(int)

        if not start_indices.tolist() or not end_indices.tolist():
            return pd.DataFrame()  # return empty df if this station doesn't have the date range

        start_idx = start_indices[0]
        end_idx = end_indices[0]

        # no end idx here if end_date > last date in df
        return df.loc[start_idx:end_idx, :]

    @staticmethod
    def get_weather_station_ids(df):
        """Get a unique list of weather station ids"""
        return df.station_id.unique()  # get a list of all the weather station IDs

    def set_weather_data(self):
        """sets self.weather_data"""
        self.weather_data = self.import_data()

    @staticmethod
    def import_data():
        """Unzips the zipfile if it hasn't been already, reads in the csv as a pandas dataframe"""
        if os.path.exists(FILE_PATH):  # check if zip file has already been unzipped
            df = pd.read_csv(FILE_PATH)  # if so, read it in as a pandas df
        else:
            with ZipFile(FILE_PATH + '.zip', 'r') as zipObj:
                zipObj.extractall(FILE_DIR)  # extract all the contents of zip file in same directory
                df = pd.read_csv(FILE_PATH)  # read it in as pandas df

        # cleaned_data = self.clean_data(df)
            # I meant to come back to this but ran out of time
            # convert the station IDs to ints
            # convert the dates to floats with three decimals / fixes the decimals on the import
            # do some data validity checks i.e. no weird characters, missing values etc.

        # return_cleaned_data
        return df


if __name__ == '__main__':
    solution = WeatherAnalysisSolution()
    solution.set_weather_data()

    # Part One
    q_one_station_id, q_one_date = solution.find_lowest_temp_station_date()
    print(f"Station {q_one_station_id} had the lowest temperature on {q_one_date} \n")

    # Part Two
    q_two_station_id = solution.find_station_with_most_fluctuation()
    print(f"Station {q_two_station_id} had the most temperature fluctuation \n")

    # Part Three
    first_date = 2000.375  # just an example
    second_date = 2000.958
    q_three_station_id = solution.find_station_with_most_fluctuation_date_range(first_date, second_date)
    print(f"Station {q_three_station_id} had the most temperature fluctuation between {first_date} and {second_date} \n")
