
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 项目根目录
PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data"
IMAGE_DIR = PROJECT_DIR / "images"

# 读取小时需求分析结果
df = pd.read_csv(
    DATA_DIR / "taxi_hourly_demand.csv"
)

# 中文字体设置
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 区分工作日和周末
weekday = df[df["is_weekend"] == False]
weekend = df[df["is_weekend"] == True]

# 绘制小时订单需求曲线
plt.plot(
    weekday["hour"],
    weekday["avg_daily_trips"],
    label="工作日"
)

plt.plot(
    weekend["hour"],
    weekend["avg_daily_trips"],
    label="周末"
)

plt.xlabel("Hour")
plt.ylabel("Average Daily Trips")
plt.title("Hourly Taxi Demand")
plt.xticks(range(24))
plt.legend()

# 保存图片
plt.savefig(
    IMAGE_DIR / "taxi_hourly_demand.png",
    dpi=150,
    bbox_inches="tight"
)

plt.show()

print("小时订单需求图生成成功")
