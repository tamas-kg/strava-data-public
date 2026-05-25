from src.streamlit import StreamlitDash
from src.postgres_db import PostgresDB
from src.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

def overview_page():
    postgres_db = PostgresDB(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    dash = StreamlitDash(postgres_db)

    map_data = dash.get_map_data()
    m = dash.build_route_map(map_data)
    dash.render_responsive_map(m)

    # Get a fresh copy to avoid modifying session state directly
    df_monthly = dash.get_monthly_data().copy()
    dash.display_monthly_data(df_monthly)