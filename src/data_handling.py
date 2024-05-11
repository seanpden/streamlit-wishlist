import polars as pl


def load_data(sheets_url):
    csv_url: str = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    df = pl.read_csv(csv_url, truncate_ragged_lines=True).filter(
        pl.col("Purchased") != True
    )
    df.select("Amount").cast({"Amount": pl.Decimal(scale=2, precision=8)})
    df.drop_in_place("Purchased")
    df.drop_in_place("Want/Amt")
    df.drop_in_place("norm r/a")
    return df.sort("Efficiency Rank")


def compute_metrics(data: pl.DataFrame):
    count_of_items = data.select(pl.count()).item()

    most_effecient_item = (
        data.filter(pl.col("Efficiency Rank") == pl.min("Efficiency Rank"))
        .row(0, named=True)
        .get("Item")
    )

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
        "most_effecient_item": most_effecient_item,
        "cheapest_item": cheapest_item,
        "expensive_item": expensive_item,
    }

    return ret
