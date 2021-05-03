import pytest
import datetime


@pytest.fixture
def mock_timeseries(mocker):
    """Simulate getting a timeseries in JSON format."""

    def _mock_timeseries(json_file):
        mocker.patch("seriesbr.helpers.timeseries.get_json", return_value=json_file)

    return _mock_timeseries


@pytest.fixture
def mock_metadata(mocker):
    """Simulate getting timeseries metadata in JSON format."""

    def _mock_metadata(json_file):
        mocker.patch("seriesbr.helpers.metadata.get_json", return_value=json_file)

    return _mock_metadata


@pytest.fixture
def mock_search_results(mocker):
    """Simulate getting a search result in JSON format."""

    def _mock_search_results(json_file):
        mocker.patch("seriesbr.helpers.search_results.get_json", return_value=json_file)

    return _mock_search_results


@pytest.fixture
def mock_today(mocker):
    date = datetime.datetime(2019, 12, 2)

    mocker.patch("seriesbr.helpers.dates.get_today_date", return_value=date)
