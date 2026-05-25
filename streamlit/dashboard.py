import streamlit as st
from src import overview_page
from src import segment_page

if 'stored_route_map' not in st.session_state:
    st.session_state['stored_route_map'] = None

def main():

    st.markdown(
        """
        <style>
            /* Main container styling */
            section.stMain .block-container {
                max-width: 1000px;
                padding-top: 1rem;    /* Adjust vertical spacing */
                padding-bottom: 1rem; /* Adjust bottom spacing */
                padding-left: 0rem;
                padding-right: 0rem;
            }
            /* Optional: reduce header bar height */
            header.stAppHeader {
                padding-top: 0.5rem;
                padding-bottom: 0.5rem;
            }
            /* Completely remove default margins (use if needed) */
            html, body, .block-container {
                margin: 0;
                padding: 0;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    pages = [
        st.Page(overview_page.overview_page, title="Overview", icon="🗺️", default=True),
        st.Page(segment_page.segment_page, title="Segment View", icon="🏅")
    ]

    current_page = st.navigation(pages)
    current_page.run()

if __name__ == "__main__":
    main()
