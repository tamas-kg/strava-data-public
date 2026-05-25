from src.postgres_db import PostgresDB
import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
import numpy as np
import pandas as pd
from pandas import DataFrame
import plotly.express as px
import folium
from streamlit.components.v1 import html as st_html
import altair as alt
import decimal

class StreamlitDash:
    def __init__(self, db: PostgresDB):
        self.db = db

    def get_segment_data(self) -> DataFrame:
        if 'segment_data' not in st.session_state:
            data, colnames = self.db.retrieve_segment_effort_data()

            df = pd.DataFrame(data, columns=colnames)
            df['start_date'] = pd.to_datetime(df['start_date'], utc=True)
            df['elapsed_time'] = pd.to_timedelta(df['elapsed_time'])

            df['rank'] = df.groupby('segment_id')['elapsed_time'].rank(ascending=True, method='dense')

            conditions = [
                    df['rank'] == 1,
                    df['rank'] == 2,
                    df['rank'] == 3
            ]
            choices = ['#FFD700', '#C0C0C0', '#CD7F32']

            df['color'] = np.select(conditions, choices, default='#3B82F6')
            df['size'] = 10

            df['start_date_day'] = df['start_date'].dt.strftime('%Y-%m-%d %H:%M')
            df['elapsed_time_seconds'] = df['elapsed_time'].dt.total_seconds()
            df['elapsed_time'] = df['elapsed_time'].dt.seconds.apply(self.format_duration)
            df = df[['name','start_date','start_date_day','elapsed_time','elapsed_time_seconds','rank', 'color', 'size']]

            st.session_state.segment_data = df

        return st.session_state.segment_data
    
    def get_map_data(self) -> DataFrame:
        if 'map_data' not in st.session_state:
            data, colnames = self.db.retrieve_map_data()

            df = pd.DataFrame(data, columns=colnames)
            st.session_state.map_data = df
        return st.session_state.map_data
    
    def get_monthly_data(self) -> DataFrame:
        if 'monthly_data' not in st.session_state:
            data, colnames = self.db.retrieve_gold_monthly()

            df = pd.DataFrame(data, columns=colnames)
            st.session_state.monthly_data = df
        return st.session_state.monthly_data
        
    def build_route_map(self, map_data:DataFrame) -> folium.Map:
        if 'route_map' not in st.session_state:
            m = folium.Map(location=[47.51984000,19.02218000], zoom_start=12)
            FeatureGroup = folium.FeatureGroup(name="Routes")
            for _, row in map_data.iterrows():
                folium.GeoJson(row['geojson_geom']).add_to(FeatureGroup)
            FeatureGroup.add_to(m)

            st.session_state.route_map = m

        return st.session_state.route_map


    def format_duration(self, seconds: int) -> str:
        """"Format seconds as minutes and seconds """
        minutes, secs = divmod(int(seconds), 60)
        parts = []
        if minutes:
            parts.append(f"{minutes}m")
        parts.append(f"{secs}s")
        return " ".join(parts)
    
    def format_time_h_m(self, td) -> str:
        """ Format timedelta as string """
        total_seconds = td.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        return f"{hours}h {minutes}m"

    def render_responsive_map(self, m: folium.Map, height: int = 600):
        st.title("Strava Dashboard")
        map_html = m._repr_html_()
        responsive_html = f"""
        <style>
        .responsive-map {{
            position: relative;
            padding-bottom: 75%; /* Adjust aspect ratio */
            height: 0;
            overflow: hidden;
        }}
        .responsive-map iframe {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }}
        </style>
        <div class="responsive-map">
        {map_html}
        </div>
        """
        st_html(responsive_html, height=height)

    def display_segment_data(self, df: DataFrame):
        
        st.title("Strava Dashboard")

        options_list = df['name'].unique().tolist()
        options = [o.replace('"','') for o in options_list]
        options.sort()
        selection = st.selectbox(f"Filter by Segment name:", options)

        def get_rank_time(segment_df:DataFrame, rank:int) -> str:
            """ Return rank value and handle cases where it doesn't exist """

            row = segment_df.loc[segment_df['rank'] == rank, 'elapsed_time']
            return str(row.iloc[0]) if not row.empty else "N/A"
        
        segment_df = df[df['name'] == selection]

        gold = get_rank_time(segment_df, 1)
        silver = get_rank_time(segment_df, 2)
        bronze = get_rank_time(segment_df, 3)
    

        df = df[['start_date','start_date_day','elapsed_time','elapsed_time_seconds','rank','color','size']][df['name'] == selection]


        col1, col2, col3 = st.columns(3)

        col1.metric(label="Gold", value=gold)
        col2.metric(label="Silver", value=silver)
        col3.metric(label="Bronze", value=bronze)

        style_metric_cards(
            background_color="#000000",
            border_left_color="#3B82F6"
        )
        fig = px.scatter(df, title='Segment Efforts', x='start_date', y='elapsed_time_seconds', color='color', 
                         labels={'start_date_day':'Date', 'elapsed_time_seconds':'Duration'},
                         hover_data={'start_date_day':True,'elapsed_time':True,'elapsed_time_seconds':False,'size':False,'start_date':False}, 
                         size='size', size_max=10, opacity=0.6,
                         color_discrete_map='identity')


        st.plotly_chart(fig)
        
        st.dataframe(df.drop(columns=['elapsed_time_seconds','rank','color','size', 'start_date']), hide_index=True)

    def display_monthly_data(self, df_monthly:DataFrame) -> None:
            # Fix: Convert Decimal columns to float for Altair
        for col in ['total_distance', 'total_elevation', 'total_calories']:
            if df_monthly[col].dtype == object and df_monthly[col].apply(lambda x: isinstance(x, decimal.Decimal)).any():
                df_monthly[col] = df_monthly[col].astype(float)

        # Convert total_time (Timedelta) to total hours for plotting
        df_monthly['total_time'] = pd.to_timedelta(df_monthly['total_time'])
        df_monthly['total_time_hours'] = df_monthly['total_time'].dt.total_seconds() / 3600

        # Ensure month_name is ordered categorically for x-axis
        month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        df_monthly['month_name'] = pd.Categorical(df_monthly['month_name'], categories=month_order, ordered=True)

        # UI: Select metric from sidebar
        metrics = ['total_distance', 'total_time', 'total_elevation', 'total_calories', 'total_prs']
        selected_metric = st.selectbox("Select Metric", metrics, key="metric_select_altair")

        # Fix for Altair: use string-formatted time for tooltip
        df_monthly['total_time_str'] = df_monthly['total_time'].apply(self.format_time_h_m)

        # Logic to use correct column for Y-axis
        if selected_metric == 'total_time':
            y_col = 'total_time_hours'
            tooltip_col = 'total_time_str'
        else:
            y_col = selected_metric
            tooltip_col = selected_metric

        # Altair chart
        chart = alt.Chart(df_monthly).mark_bar().encode(
            x=alt.X('month_name:N', title='Month', sort=month_order),
            y=alt.Y(f'{y_col}:Q', title=selected_metric.replace('_', ' ').title()),
            color=alt.Color('year:N', title='Year'),
            xOffset='year:N',  # group bars by year
            tooltip=['month_name', 'year', tooltip_col]
        ).properties(
            width=600,
            height=400,
            title=f'Monthly {selected_metric.replace("_", " ").title()} Comparison by Year'
        ).configure_axis(
            labelAngle=0
        )

        # Render chart in Streamlit

        st.altair_chart(chart, use_container_width=True)


