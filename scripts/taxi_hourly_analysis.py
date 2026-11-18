
import pandas as pd
from pathlib import Path

# 项目根目录
PROJECT_DIR = Path(__file__).resolve().parents[1]

# 数据目录
DATA_DIR = PROJECT_DIR / "data"

# 读取数据
df = pd.read_csv(
    DATA_DIR / "taxi_business_jan2021.csv",
    parse_dates=["tpep_pickup_datetime"]
)

df["hour"] = df["tpep_pickup_datetime"].dt.hour
df["is_weekend"] = df["tpep_pickup_datetime"].dt.dayofweek >= 5

# 按工作日、周末和小时统计订单量
hourly_count = (
    df.groupby(["is_weekend", "hour"])
    .size()
    .reset_index(name="trip_count")
)

# 2021年1月工作日和周末天数
days_map = {
    False: 21,
    True: 10
}

hourly_count["days"] = hourly_count["is_weekend"].map(days_map)

hourly_count["avg_daily_trips"] = (
    hourly_count["trip_count"] / hourly_count["days"]
)

# 数据验证
print("分组行数：", len(hourly_count))
print("平均值缺失：", hourly_count["avg_daily_trips"].isna().sum())
print("原始订单总数：", len(df))
print("分组订单总数：", hourly_count["trip_count"].sum())

# 导出结果
hourly_count.to_csv(
    DATA_DIR / "taxi_hourly_demand.csv",
    index=False
)

print("订单需求分析完成，文件已导出")
