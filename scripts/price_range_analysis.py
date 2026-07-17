import pandas as pd
from pathlib import Path

ROOT = Path(__file__).parent
DATA_PATH = ROOT / "淘宝全品类全国数据.csv"
OUTPUT_DIR = ROOT / "output" / "day03_analysis"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)

price_below_500 = (df["商品价格"] < 500).sum()
price_500_to_1000 = ((df["商品价格"] >= 500) & (df["商品价格"] <= 1000)).sum()

result = pd.DataFrame({
    "价格区间": ["低于500元", "500-1000元"],
    "商品数": [price_below_500, price_500_to_1000]
})

output_path = OUTPUT_DIR / "price_range_count.csv"
result.to_csv(output_path, index=False, encoding="utf-8-sig")

print("价格区间统计结果：")
print(result)
print(f"\n结果已保存到：{output_path}")