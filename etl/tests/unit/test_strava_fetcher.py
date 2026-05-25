import responses
from unittest.mock import patch, mock_open
from src.strava_fetcher import StravaFetcher


@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data='{"access_token":"abc","expires_at":9999999999}'
)
def test_refresh_api_token_uses_existing_token(mock_file):

    fetcher = StravaFetcher("client", "secret")

    headers = fetcher.refresh_api_token()

    assert headers == {
        "Authorization": "Bearer abc"
    }

@responses.activate
@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data='{"refresh_token":"old","expires_at":0}'
)
def test_refresh_expired_token(mock_file):

    responses.add(
        responses.POST,
        "https://www.strava.com/oauth/token",
        json={
            "access_token": "new_token",
            "refresh_token": "new_refresh",
            "expires_at": 9999999999
        },
        status=200
    )

    fetcher = StravaFetcher("client", "secret")

    headers = fetcher.refresh_api_token()

    assert headers == {
        "Authorization": "Bearer new_token"
    }

@responses.activate
@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data='{"access_token":"abc","expires_at":9999999999}'
)
def test_get_activities(mock_file):

    responses.add(
        responses.GET,
        "https://www.strava.com/api/v3/activities/",
        json=[{"id": 1}],
        status=200
    )

    fetcher = StravaFetcher("client", "secret")

    activities = fetcher.get_activities(headers={})

    # Verify request behavior
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == \
        "https://www.strava.com/api/v3/activities/"

    # Verify returned data
    assert len(activities) == 1
    assert activities[0]["id"] == 1

@responses.activate
@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data='{"access_token":"abc","expires_at":9999999999}'
)
def test_get_activities_historical(mock_file):

    responses.add(
        responses.GET,
        "https://www.strava.com/api/v3/activities/",
        json=[{"id": 1}],
        status=200
    )

    responses.add(
        responses.GET,
        "https://www.strava.com/api/v3/activities/",
        json=[],
        status=200
    )

    fetcher = StravaFetcher("client", "secret")

    activities = fetcher.get_activities({}, historical_load=True)

    assert len(activities) == 1

@responses.activate
@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data='{"access_token":"abc","expires_at":9999999999}'
)
def test_get_activity(mock_file):

    responses.add(
        responses.GET,
        "https://www.strava.com/api/v3/activities/123",
        json={"id": 123},
        status=200
    )

    fetcher = StravaFetcher("client", "secret")

    activity = fetcher.get_activity(123)

    assert activity["id"] == 123
    


