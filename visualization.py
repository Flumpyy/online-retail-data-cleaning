import os
import pandas as pd
import matplotlib.pyplot as plt


# ==============================
# 1. 讀取清理後資料
# ==============================

df = pd.read_csv(
    "clean_online_retail_final.csv",
    encoding="utf-8-sig"
)

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

print("資料讀取完成")
print("資料筆數：", len(df))


# ==============================
# 2. 建立 figures 資料夾
# ==============================

os.makedirs("figures", exist_ok=True)


# ==============================
# 3. 每月營收趨勢
# ==============================

df["YearMonth"] = df["InvoiceDate"].dt.to_period("M")

monthly_revenue = (
    df.groupby("YearMonth")["TotalPrice"]
    .sum()
)

plt.figure(figsize=(12, 6))

monthly_revenue.plot()

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    "figures/monthly_revenue.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("完成：Monthly Revenue Trend")


# ==============================
# 4. 營收最高商品 Top 10
# ==============================

top_products_revenue = (
    df.groupby("Description")["TotalPrice"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

plt.figure(figsize=(10, 6))

top_products_revenue.plot(kind="barh")

plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Product")
plt.tight_layout()

plt.savefig(
    "figures/top_products_revenue.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("完成：Top 10 Products by Revenue")


# ==============================
# 5. 銷量最高商品 Top 10
# ==============================

top_products_quantity = (
    df.groupby("Description")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

plt.figure(figsize=(10, 6))

top_products_quantity.plot(kind="barh")

plt.title("Top 10 Products by Quantity")
plt.xlabel("Quantity")
plt.ylabel("Product")
plt.tight_layout()

plt.savefig(
    "figures/top_products_quantity.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("完成：Top 10 Products by Quantity")


# ==============================
# 6. 各國營收 Top 10
# ==============================

country_revenue = (
    df.groupby("Country")["TotalPrice"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

plt.figure(figsize=(10, 6))

country_revenue.plot(kind="barh")

plt.title("Top 10 Countries by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Country")
plt.tight_layout()

plt.savefig(
    "figures/country_revenue.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("完成：Top 10 Countries by Revenue")


# ==============================
# 7. 每小時訂單量
# ==============================

df["Hour"] = df["InvoiceDate"].dt.hour

hourly_orders = (
    df.groupby("Hour")["InvoiceNo"]
    .nunique()
)

plt.figure(figsize=(10, 6))

hourly_orders.plot(kind="bar")

plt.title("Orders by Hour")
plt.xlabel("Hour")
plt.ylabel("Number of Orders")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    "figures/hourly_orders.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("完成：Orders by Hour")


# ==============================
# 8. 完成
# ==============================

print("\n==============================")
print("5 張視覺化圖表全部完成")
print("==============================")

print("""
已產生：
1. figures/monthly_revenue.png
2. figures/top_products_revenue.png
3. figures/top_products_quantity.png
4. figures/country_revenue.png
5. figures/hourly_orders.png
""")