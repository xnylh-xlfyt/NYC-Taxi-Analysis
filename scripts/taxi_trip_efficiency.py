
import pandas as pd
import numpy as np
from pathlib import Path

# 项目根目录
PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data"

# 1. 读取清洗后的业务数据
file_path = DATA_DIR / "taxi_business_jan2021.csv"
df = pd.read_csv(file_path)

# 2. 检查计算速度需要的字段
required_cols = ["clean_trip_distance", "clean_duration_min"]

for col in required_cols:
    print(f"{col} 空值数：", df[col].isna().sum())

# 3. 计算行程速度
df["trip_speed_mph"] = (
    df["clean_trip_distance"] * 60 / df["clean_duration_min"]
)

# 无效速度：距离或时长无效
invalid = (
    df["clean_trip_distance"].isna()
    | df["clean_duration_min"].isna()
    | (df["clean_trip_distance"] <= 0)
    | (df["clean_duration_min"] <= 0)
)

# 高速待检查
review_high = df["trip_speed_mph"] > 80

df["speed_status"] = np.select(
    [invalid, review_high],
    ["invalid", "review_high"],
    default="valid"
)

# 4. 提取时间维度
df["tpep_pickup_datetime"] = pd.to_datetime(
    df["tpep_pickup_datetime"]
)

df["hour"] = df["tpep_pickup_datetime"].dt.hour
df["is_weekend"] = (
    df["tpep_pickup_datetime"].dt.dayofweek >= 5
)

# 5. 只保留有效速度
df["valid_speed_mph"] = df["trip_speed_mph"].where(
    df["speed_status"] == "valid"
)

# 6. 按工作日、周末和小时进行聚合
hourly_amount = (
    df.groupby(["is_weekend", "hour"])
    .agg(
        trip_count=("total_amount", "size"),
        valid_speed_count=("valid_speed_mph", "count"),
        median_speed_mph=("valid_speed_mph", "median")
    )
    .reset_index()
)

# 7. 找出工作日和周末速度中位数最低的时段
hourly_amount_week = hourly_amount[
    hourly_amount["is_weekend"] == False
]

hourly_amount_weekend = hourly_amount[
    hourly_amount["is_weekend"] == True
]

week_min = hourly_amount_week.loc[
    hourly_amount_week["median_speed_mph"].idxmin()
]

weekend_min = hourly_amount_weekend.loc[
    hourly_amount_weekend["median_speed_mph"].idxmin()
]

print(week_min)
print(weekend_min)

# 8. 导出分析结果
hourly_amount.to_csv(
    DATA_DIR / "taxi_trip_efficiency_hourly.csv",
    index=False
)

print("行程效率分析完成，文件已导出")
