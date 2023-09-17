import streamlit as st
import os
import polars as pl
from dotenv import load_dotenv

CURRENT_DIR = os.path.realpath(os.path.dirname(__file__))
CSS_FILE = f"{CURRENT_DIR}/src/styles/main.css"
PAGE_TITLE = "Wishlist"
PAGE_ICON = "🎁"

SHEETS_URL = os.environ.get("SHEETS_URL")


def inject_css():
    with open(CSS_FILE) as f:
        st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)


def handle_page_config():
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout="wide",
        initial_sidebar_state="collapsed",
    )


def load_data(sheets_url):
    csv_url: str = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    df = pl.read_csv(csv_url, truncate_ragged_lines=True)
    df.select("Amount").cast({"Amount": pl.Decimal(scale=2, precision=8)})
    return df


def format_header():
    with st.container():
        st.markdown(
            "<h2 style='text-align: right'>Sean's Wishlist | 🎁</h2>",
            unsafe_allow_html=True,
        )
        st.markdown("---")


def compute_metrics(data):
    count_of_items = data.select(pl.count()).item()
    sum_of_items = data.select(pl.sum("Amount")).item()

    cheapest_item = (
        data.filter(pl.col("Amount") == pl.min("Amount"))
        .row(0, named=True)
        .get("Amount")
    )

    expensive_item = (
        data.filter(pl.col("Amount") == pl.max("Amount"))
        .row(0, named=True)
        .get("Amount")
    )

    ret = {
        "count_of_items": count_of_items,
        "sum_of_items": sum_of_items,
        "cheapest_item": cheapest_item,
        "expensive_item": expensive_item,
    }

    return ret


def format_metrics(count_of_items, sum_of_items, cheapest_item, expensive_item):
    col0, col1, col2, col3 = st.columns(4)

    with col0:
        st.metric(label="Count of items", value=count_of_items)
    with col1:
        st.metric(label="Sum of all items", value=f"{sum_of_items:.2f}")
    with col2:
        st.metric(label="Cheapest item", value=f"{cheapest_item:.2f}")
    with col3:
        st.metric(label="Most expensive item", value=f"{expensive_item}")


def format_dataframe(data):
    with st.container():
        st.dataframe(
            data=data,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Amount": st.column_config.NumberColumn("Amount", format="$%.2f")
            },
        )


def main():
    data = load_data(SHEETS_URL)

    load_dotenv()
    handle_page_config()
    inject_css()

    metrics_dict = compute_metrics(data)

    format_header()
    format_metrics(
        metrics_dict.get("count_of_items"),
        metrics_dict.get("sum_of_items"),
        metrics_dict.get("cheapest_item"),
        metrics_dict.get("expensive_item"),
    )
    format_dataframe(data)


if __name__ == "__main__":
    main()
