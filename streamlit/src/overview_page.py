from src.streamlit import StreamlitDash

def overview_page():
    dash = StreamlitDash()

    map_data = dash.get_map_data()
    m = dash.build_route_map(map_data)
    dash.render_responsive_map(m)

    # Get a fresh copy to avoid modifying session state directly
    df_monthly = dash.get_monthly_data().copy()
    dash.display_monthly_data(df_monthly)