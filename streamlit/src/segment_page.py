from src.streamlit import StreamlitDash
from src.postgres_db import PostgresDB
from src.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

def segment_page():
    postgres_db = PostgresDB(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    dash = StreamlitDash(postgres_db)
    df = dash.get_segment_data()
    dash.display_segment_data(df)