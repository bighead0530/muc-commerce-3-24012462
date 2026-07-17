from pathlib import Path

import pandas as pd
import numpy as np

pd.set_option("display.max_columns", None)
pd.set_option("display.float_format", lambda x: f"{x:.2f}")

DATA_PATH = Path("E Commerce Dataset.xlsx")

if not DATA_PATH.exists():
    raise FileNotFoundError("未找到 E Commerce Dataset.xlsx")

df = pd.read_excel(DATA_PATH, sheet_name="E Comm")
print(f"读取文件：{DATA_PATH}")
print(f"数据形状：{df.shape[0]} 行，{df.shape[1]} 列")

print("\n--- 数据基本信息 ---")
df.info()

print("\n--- 任务 2：生成缺失值报告 ---")
missing_report = pd.DataFrame({
    "缺失数量": df.isna().sum(),
    "缺失比例": (df.isna().mean() * 100).round(2).astype(str) + "%"
}).sort_values("缺失数量", ascending=False)
print(missing_report)

print("\n--- 任务 3：检查重复记录 ---")
duplicate_rows = df.duplicated().sum()
duplicate_customer_ids = df["CustomerID"].duplicated().sum()
print("完全重复行数：", duplicate_rows)
print("CustomerID 重复数量：", duplicate_customer_ids)

print("\n--- 任务 4：用中位数填补数值缺失 ---")
numeric_missing_cols = [
    "Tenure",
    "WarehouseToHome",
    "HourSpendOnApp",
    "OrderAmountHikeFromlastYear",
    "CouponUsed",
    "OrderCount",
    "DaySinceLastOrder",
]

for col in numeric_missing_cols:
    median = df[col].median()
    df[col] = df[col].fillna(median)
    print(f"{col} 中位数填补完成，中位数为: {median:.2f}")

print("\n填补后剩余缺失值数量：")
print(df[numeric_missing_cols].isna().sum())

print("\n--- 任务 5：查看类别取值 ---")
category_cols = [
    "PreferredLoginDevice",
    "PreferredPaymentMode",
    "PreferedOrderCat",
]

for col in category_cols:
    print(f"\n{col}")
    print(df[col].value_counts())

print("\n--- 任务 6：统一同义类别 ---")
df["PreferredLoginDevice"] = df["PreferredLoginDevice"].replace({"Phone": "Mobile Phone", "Mobile": "Mobile Phone"})
df["PreferredPaymentMode"] = df["PreferredPaymentMode"].replace({"COD": "Cash on Delivery", "CC": "Credit Card"})
df["PreferedOrderCat"] = df["PreferedOrderCat"].replace({"Mobile": "Mobile Phone"})

print("\n标准化后类别频数：")
for col in category_cols:
    print(f"\n{col}")
    print(df[col].value_counts())

print("\n--- 任务 7：检查候选异常值 ---")
def iqr_outlier_summary(series):
    series = series.dropna()
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    return pd.Series({
        "Q1": q1,
        "Q3": q3,
        "下限": lower,
        "上限": upper,
        "候选异常值数量": ((series < lower) | (series > upper)).sum()
    })

print("\nWarehouseToHome 异常值检查：")
print(iqr_outlier_summary(df["WarehouseToHome"]))

print("\nOrderCount 异常值检查：")
print(iqr_outlier_summary(df["OrderCount"]))

print("\nCashbackAmount 异常值检查：")
print(iqr_outlier_summary(df["CashbackAmount"]))

print("\n--- 任务 8：业务规则检查 ---")
rules = {
    "使用时长小于 0": (df["Tenure"] < 0).sum(),
    "仓库距离小于 0": (df["WarehouseToHome"] < 0).sum(),
    "订单数小于或等于 0": (df["OrderCount"] <= 0).sum(),
    "返现金额小于 0": (df["CashbackAmount"] < 0).sum(),
}
print(pd.Series(rules))

print("\n--- 清洗结果验收 ---")
assert df[numeric_missing_cols].isna().sum().sum() == 0, "数值字段仍有缺失值"
assert "Phone" not in df["PreferredLoginDevice"].unique(), "登录设备尚未统一"
assert "COD" not in df["PreferredPaymentMode"].unique(), "支付方式尚未统一"
assert "CC" not in df["PreferredPaymentMode"].unique(), "支付方式尚未统一"
assert "Mobile" not in df["PreferedOrderCat"].unique(), "订单品类尚未统一"

print("数据清洗验收通过。")

print("\n--- 任务 9：导出清洗后的数据 ---")
OUTPUT_PATH = Path("output/ecommerce_customer_cleaned.csv")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

print(f"已导出：{OUTPUT_PATH.resolve()}")
print(f"清洗后数据形状：{df.shape[0]} 行，{df.shape[1]} 列")