import os
import subprocess
import pytest
from testcontainers.postgres import PostgresContainer

DBT_PROJECT_DIR = "/app"  # inside container, adjust if needed

@pytest.fixture(scope="module")
def dbt_postgres():
    """Spin up a temporary Postgres for dbt to run against."""
    with PostgresContainer("strava-postgis:latest") as postgres:
        os.environ["DBT_PROFILES_DIR"] = DBT_PROJECT_DIR
        os.environ["POSTGRES_HOST"] = postgres.get_container_host_ip()
        os.environ["POSTGRES_PORT"] = str(postgres.get_exposed_port(5432))
        os.environ["POSTGRES_DB"] = postgres.dbname
        os.environ["POSTGRES_USER"] = postgres.username
        os.environ["POSTGRES_PASSWORD"] = postgres.password

        # Connect directly to populate minimal bronze tables for testing
        import psycopg2
        conn = psycopg2.connect(
            host=os.environ["POSTGRES_HOST"],
            port=os.environ["POSTGRES_PORT"],
            dbname=os.environ["POSTGRES_DB"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
        )
        cur = conn.cursor()

        with conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS postgis;")

            # Create minimal bronze schema/tables
            cur.execute("CREATE SCHEMA IF NOT EXISTS strava_bronze;")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS strava_bronze.activities_detailed (
                    id BIGINT PRIMARY KEY,
                    raw_data JSONB
                );
            """)
            # Insert minimal test data
            cur.execute("""
                INSERT INTO strava_bronze.activities_detailed (id, raw_data)
                VALUES
                (1, '{
                    "id": 1,
                    "name": "Test Ride",
                    "type": "Ride",
                    "start_date": "2025-01-01T10:00:00Z",
                    "distance": 1000,
                    "moving_time": 100,
                    "elapsed_time": 100,
                    "calories": 100,
                    "pr_count": 1,
                    "map": {"id": "123", "polyline": "xyz"},
                    "start_latlng": [0,0],
                    "end_latlng": [1,1]
                }'::jsonb);
            """)
            conn.commit()

        conn.close()

        yield postgres  # provide to tests


def test_dbt_models(dbt_postgres):
    """Run dbt models and schema tests inside the test container."""
    # Run dbt compile/build
    result = subprocess.run(
        ["dbt", "run", "--profiles-dir", DBT_PROJECT_DIR, "--project-dir", DBT_PROJECT_DIR, "--target", "test"],
        capture_output=True,
        text=True,
        check=True
    )
    print(result.stdout)
    print(result.stderr)
    assert result.returncode == 0, "dbt run failed"

    # Run dbt tests
    result = subprocess.run(
        ["dbt", "test", "--profiles-dir", DBT_PROJECT_DIR, "--project-dir", DBT_PROJECT_DIR, "--target", "test"],
        capture_output=True,
        text=True,
        check=True
    )
    print(result.stdout)
    print(result.stderr)
    assert result.returncode == 0, "dbt tests failed"