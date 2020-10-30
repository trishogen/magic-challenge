import pytest
import unittest.mock as mock
from _pytest.monkeypatch import MonkeyPatch
from weather_station_analysis.weather_station_analysis import WeatherAnalysisSolution


import pandas as pd

test_data = [
    [1, 2000.001, 5],  # station 1 example case
    [1, 2000.123, 0],  # station 1 example case
    [1, 2000.456, 5],  # station 1 example case
    [2, 2000.001, 20],
    [2, 2000.002, 15],
    [2, 2000.003, -10],
    [2, 2000.456, -10],
    [3, 2000.001, 17],
    [3, 2000.002, 20],
    [3, 2000.003, -1],
]
test_dataframe = pd.DataFrame(data=test_data, columns=['station_id', 'date', 'temperature_c'])

# I would have done more parameterization of most of the tests here as well, had I not hit 2 hours


@pytest.fixture(scope='module')
def monkeymodule():
    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()


@pytest.fixture(scope='module')
def mock_data_import(monkeymodule):
    """Mock data import"""
    mock_data_import = mock.MagicMock()
    mock_data_import.import_data = mock.MagicMock(return_value=test_dataframe)
    monkeymodule.setattr(
        'weather_station_analysis.weather_station_analysis.WeatherAnalysisSolution.import_data',
        mock_data_import.import_data)


@pytest.fixture(scope='module')
def wx_sol(mock_data_import):
    """ Creates an instance of the solution class with mocked data to use for testing"""
    solution_instance = WeatherAnalysisSolution()
    solution_instance.set_weather_data()

    return solution_instance


def test_find_lowest_temp_station_date(wx_sol):
    station_actual, date_actual = wx_sol.find_lowest_temp_station_date()

    assert station_actual == 2
    assert date_actual == 2000.003 or date_actual == 2000.456


def test_find_station_with_most_fluctuation(wx_sol):
    station_actual = wx_sol.find_station_with_most_fluctuation()

    assert station_actual == 2


def test_calc_temp_fluctuation(wx_sol):
    station_one = wx_sol.filter_data_by_station(wx_sol.weather_data, 1)
    temp_flux_actual = wx_sol.calc_temp_fluctuation(station_one)

    assert temp_flux_actual == 10


def test_filter_data_by_station(wx_sol):
    actual_data = wx_sol.filter_data_by_station(wx_sol.weather_data, 1)
    actual_data_ids = actual_data.station_id.unique()

    assert len(actual_data_ids) == 1
    assert actual_data_ids[0] == 1


def test_get_weather_station_ids(wx_sol):
    actual_ids = wx_sol.get_weather_station_ids(wx_sol.weather_data)

    assert actual_ids.tolist() == [1, 2, 3]


def test_find_station_with_most_fluctuation_date_range(wx_sol):
    station_actual = wx_sol.find_station_with_most_fluctuation_date_range(2000.001, 2000.456)

    assert station_actual == 2


def test_calc_station_fluctuation_date_range(wx_sol):
    flux_actual = wx_sol.calc_station_fluctuation_date_range(1, 2000.001, 2000.456)

    assert flux_actual == 10


def test_filter_station_data_by_date_range(wx_sol):
    station_data = wx_sol.filter_data_by_station(wx_sol.weather_data, 1)
    filtered_data_actual = wx_sol.filter_station_data_by_date_range(station_data, 2000.001, 2000.456)

    assert station_data.equals(filtered_data_actual)
