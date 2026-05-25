from unittest.mock import patch
import bronze_load


@patch("bronze_load.PostgresDB")
@patch("bronze_load.StravaFetcher")
@patch("bronze_load.ActivityProcessor")
@patch("bronze_load.StarredSegmentProcessor")
def test_main_flow(
    mock_segment_processor,
    mock_activity_processor,
    mock_fetcher,
    mock_db
):

    mock_fetcher_instance = mock_fetcher.return_value

    mock_fetcher_instance.refresh_api_token.return_value = {}
    mock_fetcher_instance.get_activities.return_value = [{"id": 1}]
    mock_fetcher_instance.get_starred_segments.return_value = [{"id": 10}]

    bronze_load.main()

    mock_fetcher_instance.get_activities.assert_called_once()

    mock_activity_processor.return_value.process_activities.assert_called_once()

    mock_segment_processor.return_value.process_starred_segments.assert_called_once()

    mock_activity_processor.return_value.process_detailed_activities.assert_called_once()

    mock_db.return_value.close.assert_called_once()