import streamlit as st
import polars as pl
import os
from src import data_handling
from dotenv import load_dotenv

CURRENT_DIR = os.path.realpath(os.path.dirname(__file__))
CSS_FILE = f"{CURRENT_DIR}/src/styles/main.css"
PAGE_TITLE = "Wishlist"
PAGE_ICON = "🎁"


def inject_css():
    with open(CSS_FILE) as f:
        _ = st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)


def handle_page_config():
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout="wide",
        initial_sidebar_state="collapsed",
    )


def render_header():
    with st.container():
        _ = st.markdown(
            "<h2>Sean's Wishlist 🎁</h2>",
            unsafe_allow_html=True,
        )
        _ = st.markdown("---")


def render_metrics(count_of_items, most_effecient_item, cheapest_item, expensive_item):
    col0, col1, col2, col3 = st.columns(4)

    with st.container():
        with col0:
            _ = st.metric(label="Count of items", value=count_of_items)
        with col1:
            _ = st.metric(label="Most effecient item", value=f"{most_effecient_item}")
        with col2:
            _ = st.metric(label="Cheapest item", value=f"${cheapest_item:.2f}")
        with col3:
            _ = st.metric(label="Most expensive item", value=f"${expensive_item:.2f}")


def render_dataframe(data: pl.DataFrame):
    with st.container():
        count = 0
        for row in data.iter_rows(named=True):
            count += 1
            with st.expander(label=f"{count}\. {row['Item']}, ${row['Amount']:.0f}"):
                st.write(f"**Want Rating**: _{row['Want (1-10)']}_")
                st.write(f"**Date Added**: _{row['Date Added']}_")
                st.write(f"**Amount**: $_{row['Amount']:.2f}_")
                st.write(f"**Link**: _{row['Link']}_")
                st.markdown("---")
                st.write(f"**Description**: _{row['Desc.']}_")
                st.write(f"**Comment**: _{row['Comments']}_")
        # st.dataframe(
        #     data=data,
        #     use_container_width=True,
        #     hide_index=True,
        #     column_config={
        #         "Amount": st.column_config.NumberColumn("Amount", format="$%.2f")
        #     },
        # )


def main():
    load_dotenv()
    SHEETS_URL = os.environ.get("SHEETS_URL")

    handle_page_config()
    inject_css()

    data = data_handling.load_data(SHEETS_URL)
    metrics_dict = data_handling.compute_metrics(data)

    render_header()
    render_metrics(
        metrics_dict.get("count_of_items"),
        metrics_dict.get("most_effecient_item"),
        metrics_dict.get("cheapest_item"),
        metrics_dict.get("expensive_item"),
    )
    render_dataframe(data)


if __name__ == "__main__":
    main()
