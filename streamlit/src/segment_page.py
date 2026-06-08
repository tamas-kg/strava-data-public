from src.streamlit import StreamlitDash

def segment_page():
    dash = StreamlitDash()
    df = dash.get_segment_data()
    dash.display_segment_data(df)