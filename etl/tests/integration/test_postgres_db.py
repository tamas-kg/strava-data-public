import json
from datetime import datetime, timezone

import pytest
from testcontainers.postgres import PostgresContainer

from src.postgres_db import PostgresDB


@pytest.fixture
def db():
    with PostgresContainer("postgres:17") as postgres:

        db = PostgresDB(
            db_name=postgres.dbname,
            db_user=postgres.username,
            db_password=postgres.password,
            db_host=postgres.get_container_host_ip(),
            db_port=postgres.get_exposed_port(5432)
        )

        create_schema_and_tables(db)

        yield db

        db.close()


def create_schema_and_tables(db):

    db.cursor.execute("""
        CREATE SCHEMA IF NOT EXISTS strava_bronze;
    """)

    db.cursor.execute("""
        CREATE TABLE strava_bronze.activities (
            id BIGINT PRIMARY KEY,
            name TEXT NOT NULL,
            start_date TIMESTAMPTZ,
            distance FLOAT,
            duration INTERVAL,
            activity_type TEXT,
            raw_data JSONB
        );
    """)

    db.conn.commit()


def make_activity(**overrides):

    activity = {
        "id": 1,
        "name": "Morning Ride",
        "start_date": "2025-01-01T10:00:00Z",
        "distance": 1000,
        "elapsed_time": 100,
        "type": "Ride"
    }

    activity.update(overrides)

    return activity


def test_insert_activity(db):

    activity = make_activity()

    db.insert_activity(
        activity,
        "strava_bronze.activities"
    )

    db.cursor.execute("""
        SELECT
            id,
            name,
            start_date,
            distance,
            EXTRACT(EPOCH FROM duration),
            activity_type,
            raw_data
        FROM strava_bronze.activities
    """)

    row = db.cursor.fetchone()

    assert row[0] == 1
    assert row[1] == "Morning Ride"

    assert row[2] == datetime(
        2025,
        1,
        1,
        10,
        0,
        tzinfo=timezone.utc
    )

    assert row[3] == 1000
    assert row[4] == 100
    assert row[5] == "Ride"

    raw_data = row[6]

    assert raw_data["name"] == "Morning Ride"
    assert raw_data["distance"] == 1000
    assert raw_data["type"] == "Ride"


def test_insert_activity_duplicate(db):

    activity = make_activity()

    db.insert_activity(activity, "strava_bronze.activities")

    db.insert_activity(activity, "strava_bronze.activities")

    db.cursor.execute("""
        SELECT COUNT(*)
        FROM strava_bronze.activities
    """)

    count = db.cursor.fetchone()[0]

    assert count == 1


@pytest.mark.parametrize(
    "activity_type",
    ["Ride", "Run", "Swim"]
)
def test_insert_multiple_activity_types(db, activity_type):

    activity = make_activity(
        id=hash(activity_type),
        type=activity_type
    )

    db.insert_activity(
        activity,
        "strava_bronze.activities"
    )

    db.cursor.execute("""
        SELECT activity_type
        FROM strava_bronze.activities
        WHERE id = %s
    """, (activity["id"],))

    result = db.cursor.fetchone()[0]

    assert result == activity_type


def test_insert_activity_invalid_timestamp(db):

    activity = make_activity(
        start_date="not-a-real-date"
    )

    with pytest.raises(ValueError):
        db.insert_activity(
            activity,
            "strava_bronze.activities"
        )


def test_insert_activity_missing_required_field(db):

    activity = make_activity()

    del activity["name"]

    with pytest.raises(KeyError):
        db.insert_activity(
            activity,
            "strava_bronze.activities"
        )


def test_duration_is_stored_correctly(db):

    activity = make_activity(
        elapsed_time=3600
    )

    db.insert_activity(
        activity,
        "strava_bronze.activities"
    )

    db.cursor.execute("""
        SELECT EXTRACT(EPOCH FROM duration)
        FROM strava_bronze.activities
        WHERE id = %s
    """, (activity["id"],))

    seconds = db.cursor.fetchone()[0]

    assert seconds == 3600


def test_raw_data_is_jsonb(db):

    activity = make_activity()

    db.insert_activity(
        activity,
        "strava_bronze.activities"
    )

    db.cursor.execute("""
        SELECT jsonb_typeof(raw_data)
        FROM strava_bronze.activities
        WHERE id = %s
    """, (activity["id"],))

    json_type = db.cursor.fetchone()[0]

    assert json_type == "object"