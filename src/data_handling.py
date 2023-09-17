import polars as pl


def load_data(sheets_url):
    csv_url: str = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    df = pl.read_csv(csv_url, truncate_ragged_lines=True).filter(
        pl.col("Purchased") != True
    )
    df.select("Amount").cast({"Amount": pl.Decimal(scale=2, precision=8)})
    return df


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
