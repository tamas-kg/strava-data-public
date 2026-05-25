from unittest.mock import patch
from src.activity_processor import ActivityProcessor


def test_process_activities_inserts_valid_activities(mock_db, mock_api):

    processor = ActivityProcessor(mock_db, mock_api)

    activities = [
        {
            "id": 1,
            "distance": 1000,
            "elapsed_time": 300
        }
    ]

    processor.process_activities(activities)

    mock_db.insert_activity.assert_called_once_with(
        activities[0],
        "strava_bronze.activities"
    )


def test_process_activities_skips_zero_distance(mock_db, mock_api):

    processor = ActivityProcessor(mock_db, mock_api)

    activities = [
        {
            "id": 1,
            "distance": 0,
            "elapsed_time": 300
        }
    ]

    processor.process_activities(activities)

    mock_db.insert_activity.assert_not_called()


def test_process_activities_skips_zero_elapsed_time(mock_db, mock_api):

    processor = ActivityProcessor(mock_db, mock_api)

    activities = [
        {
            "id": 1,
            "distance": 1000,
            "elapsed_time": 0
        }
    ]

    processor.process_activities(activities)

    mock_db.insert_activity.assert_not_called()


@patch("src.activity_processor.time.sleep", return_value=None)
def test_process_detailed_activities(mock_sleep, mock_db, mock_api):

    mock_db.retrieve_activity_ids.return_value = [101, 102]

    mock_api.get_activity.side_effect = [
        {"id": 101},
        {"id": 102}
    ]

    processor = ActivityProcessor(mock_db, mock_api)

    processor.process_detailed_activities()

    assert mock_api.get_activity.call_count == 2

    assert mock_db.insert_activity.call_count == 2

    assert mock_sleep.call_count == 2
    mock_sleep.assert_called_with(40)

    mock_db.insert_activity.assert_any_call(
        {"id": 101},
        "strava_bronze.activities_detailed"
    )

    mock_db.insert_activity.assert_any_call(
        {"id": 102},
        "strava_bronze.activities_detailed"
    )