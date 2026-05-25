from src.starred_segment_processor import StarredSegmentProcessor
from unittest.mock import call

def test_process_starred_segments(mock_db):

    processor = StarredSegmentProcessor(mock_db)

    segments = [
        {
            "id": 1,
            "name": "Test Segment"
        }
    ]

    processor.process_starred_segments(segments)

    mock_db.insert_starred_segment.assert_called_once_with(
        segments[0]
    )

def test_process_starred_segments_multiple(mock_db):
    processor = StarredSegmentProcessor(mock_db)

    segments = [
        {"id": 1, "name": "A"},
        {"id": 2, "name": "B"}
    ]

    processor.process_starred_segments(segments)

    assert mock_db.insert_starred_segment.call_count == 2

    mock_db.insert_starred_segment.assert_has_calls([
        call({"id": 1, "name": "A"}),
        call({"id": 2, "name": "B"})
    ])