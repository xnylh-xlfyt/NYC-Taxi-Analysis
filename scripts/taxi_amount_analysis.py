
import pandas as pd
from pathlib import Path

# 项目根目录
PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data"

# 读取业务数据
df = pd.read_csv(
    DATA_DIR / "taxi_business_jan2021.csv",
    parse_dates=["tpep_pickup_datetime"]
)

df["is_weekend"] = df["tpep_pickup_datetime"].dt.dayofweek >= 5
df["hour"] = df["tpep_pickup_datetime"].dt.hour

result = df.groupby("is_weekend").agg(
    order_count=("total_amount", "size"),
    revenue=("total_amount", "sum"),
    avg_order_amount=("total_amount", "mean")
).reset_index()

days_map = {
    False: 21,
    True: 10
}

result["days"] = result["is_weekend"].map(days_map)
result["avg_daily_revenue"] = result["revenue"] / result["days"]

hourly_amount = (
    df.groupby(["is_weekend", "hour"])
    .agg(
        order_count=("total_amount", "size"),
        total_amount=("total_amount", "sum"),
        avg_order_amount=("total_amount", "mean")
    )
    .reset_index()
)

hourly_amount["days"] = hourly_amount["is_weekend"].map(days_map)

hourly_amount["avg_daily_amount"] = (
    hourly_amount["total_amount"] / hourly_amount["days"]
)

weekday = hourly_amount[hourly_amount["is_weekend"] == False]
weekend = hourly_amount[hourly_amount["is_weekend"] == True]

print(weekday.loc[weekday["avg_daily_amount"].idxmax()])
print(weekend.loc[weekend["avg_daily_amount"].idxmax()])
