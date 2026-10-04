import pandas as pd

df = pd.read_excel("data/Online Retail.xlsx")

clean_df = df.copy()

print("清理前資料筆數：", len(clean_df))

print("\n完全重複資料筆數：")
print(clean_df.duplicated().sum())

before = len(clean_df)

clean_df = clean_df.drop_duplicates()

after = len(clean_df)

print("\n刪除重複資料：", before - after, "筆")
print("刪除後資料筆數：", after)

cancelled = clean_df[
    clean_df["InvoiceNo"].astype(str).str.startswith("C")
]

print("\n取消交易筆數：", len(cancelled))
print(cancelled[["InvoiceNo", "Quantity", "UnitPrice"]].head(10))

non_positive_qty = clean_df[
    (~clean_df["InvoiceNo"].astype(str).str.startswith("C"))
    & (clean_df["Quantity"] <= 0)
]

print("\n非取消交易但 Quantity <= 0 的筆數：", len(non_positive_qty))
print(non_positive_qty[
    ["InvoiceNo", "StockCode", "Description", "Quantity", "UnitPrice"]
].head(20))

print("\n1336 筆特殊資料檢查：")

print("Description 缺失：",
      non_positive_qty["Description"].isnull().sum())

print("UnitPrice = 0：",
      (non_positive_qty["UnitPrice"] == 0).sum())

print("CustomerID 缺失：",
      non_positive_qty["CustomerID"].isnull().sum())

print("\nQuantity <= 0 且有 Description 的種類：")

print(
    non_positive_qty[
        non_positive_qty["Description"].notnull()
    ]["Description"].value_counts().head(30)
)

print("\nQuantity > 0 但 UnitPrice = 0 的筆數：")

positive_zero_price = clean_df[
    (clean_df["Quantity"] > 0) &
    (clean_df["UnitPrice"] == 0)
]

print(len(positive_zero_price))

print(
    positive_zero_price[
        ["InvoiceNo", "StockCode", "Description",
         "Quantity", "UnitPrice", "CustomerID"]
    ].head(30)
)

print("\n零元正數交易分類：")

print(
    "有 CustomerID（顧客編號）：",
    positive_zero_price["CustomerID"].notnull().sum()
)

print(
    "沒有 CustomerID（顧客編號）：",
    positive_zero_price["CustomerID"].isnull().sum()
)

zero_price_customer = positive_zero_price[
    positive_zero_price["CustomerID"].notnull()
]

print("\n有 CustomerID（顧客編號）的零元交易：")

print(
    zero_price_customer[
        ["InvoiceNo", "StockCode", "Description",
         "Quantity", "UnitPrice", "CustomerID", "Country"]
    ]
)

print("\n40 筆零元交易詳細內容：")

print(
    zero_price_customer[
        ["StockCode", "Description", "Quantity", "UnitPrice"]
    ].to_string(index=False)
)

print("\n非取消且 Quantity（數量）<= 0 的 Description（商品描述）統計：")

print(
    non_positive_qty["Description"]
    .fillna("NaN（缺失值）")
    .value_counts()
    .head(30)
)

print("\n非取消且 Quantity（數量）<= 0 的 UnitPrice（單價）統計：")

print(
    non_positive_qty["UnitPrice"]
    .value_counts()
    .sort_index()
)

# 刪除非實際銷售紀錄
before = len(clean_df)

clean_df = clean_df[
    ~(
        (clean_df["Quantity"] <= 0) &
        (clean_df["UnitPrice"] == 0) &
        (~clean_df["InvoiceNo"].astype(str).str.startswith("C"))
    )
]

after = len(clean_df)

print("\n刪除非實際銷售紀錄：", before - after, "筆")
print("目前資料筆數：", after)

# 檢查取消交易
cancelled_clean = clean_df[
    clean_df["InvoiceNo"].astype(str).str.startswith("C")
]

print("\n目前 cancelled transaction（取消交易）筆數：", len(cancelled_clean))

print(
    cancelled_clean[
        ["InvoiceNo", "StockCode", "Description", "Quantity", "UnitPrice", "CustomerID"]
    ].head(20)
)

# 將取消交易另外保存
cancelled_df = clean_df[
    clean_df["InvoiceNo"].astype(str).str.startswith("C")
].copy()

# 從主要銷售資料排除取消交易
before = len(clean_df)

clean_df = clean_df[
    ~clean_df["InvoiceNo"].astype(str).str.startswith("C")
].copy()

after = len(clean_df)

print("\n保存 cancelled transaction（取消交易）：", len(cancelled_df), "筆")
print("排除取消交易：", before - after, "筆")
print("目前正常銷售資料筆數：", after)

print("\n清理後異常值檢查：")

print(
    "Quantity（數量） <= 0：",
    (clean_df["Quantity"] <= 0).sum(),
    "筆"
)

print(
    "UnitPrice（單價） <= 0：",
    (clean_df["UnitPrice"] <= 0).sum(),
    "筆"
)

print(
    "CustomerID（顧客編號）缺失：",
    clean_df["CustomerID"].isnull().sum(),
    "筆"
)

print(
    "Description（商品描述）缺失：",
    clean_df["Description"].isnull().sum(),
    "筆"
)

zero_price = clean_df[
    clean_df["UnitPrice"] <= 0
]

print("\nUnitPrice（單價） <= 0 的資料筆數：", len(zero_price))

print(
    zero_price[
        ["InvoiceNo", "StockCode", "Description",
         "Quantity", "UnitPrice", "CustomerID", "Country"]
    ].head(50).to_string(index=False)
)

print("\nUnitPrice（單價） <= 0 分類：")

print(
    "Description（商品描述）缺失：",
    zero_price["Description"].isnull().sum(),
    "筆"
)

print(
    "CustomerID（顧客編號）缺失：",
    zero_price["CustomerID"].isnull().sum(),
    "筆"
)

print(
    "Description（商品描述）和 CustomerID（顧客編號）都缺失：",
    (
        zero_price["Description"].isnull()
        & zero_price["CustomerID"].isnull()
    ).sum(),
    "筆"
)

print(
    "Description（商品描述）和 CustomerID（顧客編號）都有資料：",
    (
        zero_price["Description"].notnull()
        & zero_price["CustomerID"].notnull()
    ).sum(),
    "筆"
)

zero_price_valid = zero_price[
    zero_price["Description"].notnull()
    & zero_price["CustomerID"].notnull()
]

print("\n40 筆有完整資料但 UnitPrice（單價） = 0 的交易：")

print(
    zero_price_valid[
        ["InvoiceNo", "StockCode", "Description",
         "Quantity", "UnitPrice", "CustomerID",
         "Country", "InvoiceDate"]
    ].to_string(index=False)
)

# 保存零單價交易
zero_price_df = clean_df[
    clean_df["UnitPrice"] <= 0
].copy()

before = len(clean_df)

# 從銷售分析資料排除零單價交易
clean_df = clean_df[
    clean_df["UnitPrice"] > 0
].copy()

after = len(clean_df)

print("\n保存 zero_price_df（零單價交易資料）：", len(zero_price_df), "筆")
print("排除零單價交易：", before - after, "筆")
print("目前正常銷售資料筆數：", after)

print("\nCustomerID（顧客編號）缺失檢查：")

print(
    "CustomerID（顧客編號）缺失：",
    clean_df["CustomerID"].isnull().sum(),
    "筆"
)

print(
    "CustomerID（顧客編號）有資料：",
    clean_df["CustomerID"].notnull().sum(),
    "筆"
)

customer_missing = clean_df[
    clean_df["CustomerID"].isnull()
]

print("\nCustomerID（顧客編號）缺失資料檢查：")
print("資料筆數：", len(customer_missing), "筆")

print(
    customer_missing[
        ["InvoiceNo", "StockCode", "Description",
         "Quantity", "UnitPrice", "InvoiceDate", "Country"]
    ].head(30).to_string(index=False)
)

description_missing = clean_df[
    clean_df["Description"].isnull()
]

print("\nDescription（商品描述）缺失資料檢查：")
print("資料筆數：", len(description_missing), "筆")

print(
    description_missing[
        ["InvoiceNo", "StockCode", "Description",
         "Quantity", "UnitPrice", "CustomerID",
         "InvoiceDate", "Country"]
    ].head(50).to_string(index=False)
)

# 建立有顧客編號的資料
customer_df = clean_df[
    clean_df["CustomerID"].notnull()
].copy()

print("\n資料清理完成：")
print("clean_df（清理後銷售資料）：", len(clean_df), "筆")
print("customer_df（有顧客編號資料）：", len(customer_df), "筆")
print(
    "CustomerID（顧客編號）缺失但保留於 clean_df：",
    clean_df["CustomerID"].isnull().sum(),
    "筆"
)

# 儲存清理完成的資料
clean_df.to_csv(
    "clean_online_retail.csv",
    index=False,
    encoding="utf-8-sig"
)

customer_df.to_csv(
    "customer_online_retail.csv",
    index=False,
    encoding="utf-8-sig"
)

cancelled_df.to_csv(
    "cancelled_transactions.csv",
    index=False,
    encoding="utf-8-sig"
)

zero_price_df.to_csv(
    "zero_price_transactions.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\n資料儲存完成")

# 建立每筆交易的總金額
clean_df["TotalPrice"] = (
    clean_df["Quantity"] * clean_df["UnitPrice"]
)

print("\nTotalPrice（交易金額）建立完成")

print(
    clean_df[
        ["InvoiceNo", "Description", "Quantity",
         "UnitPrice", "TotalPrice"]
    ].head(20).to_string(index=False)
)

# ============================================================
# EDA（探索性資料分析）
# ============================================================

# ------------------------------------------------------------
# 1. 建立交易金額
# ------------------------------------------------------------

clean_df["TotalPrice"] = (
    clean_df["Quantity"] * clean_df["UnitPrice"]
)


# ------------------------------------------------------------
# 2. 處理交易日期
# ------------------------------------------------------------

clean_df["InvoiceDate"] = pd.to_datetime(
    clean_df["InvoiceDate"]
)

clean_df["Year"] = clean_df["InvoiceDate"].dt.year
clean_df["Month"] = clean_df["InvoiceDate"].dt.month
clean_df["Day"] = clean_df["InvoiceDate"].dt.day
clean_df["Hour"] = clean_df["InvoiceDate"].dt.hour

# 建立年月，例如 2011-01
clean_df["YearMonth"] = (
    clean_df["InvoiceDate"]
    .dt.to_period("M")
    .astype(str)
)


# ------------------------------------------------------------
# 3. 基本資料概況
# ------------------------------------------------------------

print("\n========== 基本資料概況 ==========")

print(
    "資料總筆數：",
    len(clean_df),
    "筆"
)

print(
    "InvoiceNo（發票／交易編號）數量：",
    clean_df["InvoiceNo"].nunique(),
    "筆"
)

print(
    "StockCode（商品代碼）數量：",
    clean_df["StockCode"].nunique(),
    "個"
)

print(
    "CustomerID（顧客編號）數量：",
    clean_df["CustomerID"].nunique(),
    "位"
)

print(
    "Country（國家）數量：",
    clean_df["Country"].nunique(),
    "個"
)


# ------------------------------------------------------------
# 4. 整體銷售指標
# ------------------------------------------------------------

total_revenue = clean_df["TotalPrice"].sum()

total_quantity = clean_df["Quantity"].sum()

total_orders = clean_df["InvoiceNo"].nunique()

average_order_value = (
    total_revenue / total_orders
)

print("\n========== 整體銷售指標 ==========")

print(
    "Total Revenue（總營收）：",
    round(total_revenue, 2)
)

print(
    "Total Quantity（總銷售數量）：",
    total_quantity
)

print(
    "Total Orders（總訂單數）：",
    total_orders
)

print(
    "Average Order Value（平均訂單金額）：",
    round(average_order_value, 2)
)


# ------------------------------------------------------------
# 5. 每月營收
# ------------------------------------------------------------

monthly_sales = (
    clean_df
    .groupby("YearMonth")["TotalPrice"]
    .sum()
    .sort_index()
)

print("\n========== Monthly Sales（每月營收） ==========")

print(
    monthly_sales.to_string()
)


# ------------------------------------------------------------
# 6. 每月訂單數
# ------------------------------------------------------------

monthly_orders = (
    clean_df
    .groupby("YearMonth")["InvoiceNo"]
    .nunique()
    .sort_index()
)

print("\n========== Monthly Orders（每月訂單數） ==========")

print(
    monthly_orders.to_string()
)


# ------------------------------------------------------------
# 7. 銷售數量最高的商品 Top 10
# ------------------------------------------------------------

top_quantity_products = (
    clean_df
    .groupby("Description")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(
    "\n========== Top 10 Products by Quantity"
    "（銷售數量最高的前 10 名商品） =========="
)

print(
    top_quantity_products.to_string()
)


# ------------------------------------------------------------
# 8. 營收最高的商品 Top 10
# ------------------------------------------------------------

top_revenue_products = (
    clean_df
    .groupby("Description")["TotalPrice"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(
    "\n========== Top 10 Products by Revenue"
    "（營收最高的前 10 名商品） =========="
)

print(
    top_revenue_products.to_string()
)


# ------------------------------------------------------------
# 9. 各國營收
# ------------------------------------------------------------

country_revenue = (
    clean_df
    .groupby("Country")["TotalPrice"]
    .sum()
    .sort_values(ascending=False)
)

print(
    "\n========== Revenue by Country"
    "（各國營收） =========="
)

print(
    country_revenue.head(15).to_string()
)


# ------------------------------------------------------------
# 10. 各國訂單數
# ------------------------------------------------------------

country_orders = (
    clean_df
    .groupby("Country")["InvoiceNo"]
    .nunique()
    .sort_values(ascending=False)
)

print(
    "\n========== Orders by Country"
    "（各國訂單數） =========="
)

print(
    country_orders.head(15).to_string()
)


# ------------------------------------------------------------
# 11. 不同時段的交易筆數
# ------------------------------------------------------------

hourly_transactions = (
    clean_df
    .groupby("Hour")
    .size()
    .sort_index()
)

print(
    "\n========== Transactions by Hour"
    "（各時段交易筆數） =========="
)

print(
    hourly_transactions.to_string()
)


# ------------------------------------------------------------
# 12. CustomerID 缺失比例
# ------------------------------------------------------------

customer_missing_count = (
    clean_df["CustomerID"]
    .isnull()
    .sum()
)

customer_missing_rate = (
    customer_missing_count
    / len(clean_df)
    * 100
)

print(
    "\n========== CustomerID（顧客編號）缺失 =========="
)

print(
    "CustomerID（顧客編號）缺失：",
    customer_missing_count,
    "筆"
)

print(
    "CustomerID（顧客編號）缺失比例：",
    round(customer_missing_rate, 2),
    "%"
)


# ------------------------------------------------------------
# 13. 建立顧客分析資料
# ------------------------------------------------------------

customer_df = clean_df[
    clean_df["CustomerID"].notnull()
].copy()

customer_summary = (
    customer_df
    .groupby("CustomerID")
    .agg(
        Orders=("InvoiceNo", "nunique"),
        Quantity=("Quantity", "sum"),
        Revenue=("TotalPrice", "sum")
    )
)

print(
    "\n========== Customer Summary"
    "（顧客消費摘要） =========="
)

print(
    customer_summary
    .sort_values("Revenue", ascending=False)
    .head(10)
    .to_string()
)


# ------------------------------------------------------------
# 14. 最終資料品質檢查
# ------------------------------------------------------------

print(
    "\n========== Final Data Check"
    "（最終資料檢查） =========="
)

print(
    "Quantity（數量）<= 0：",
    (clean_df["Quantity"] <= 0).sum(),
    "筆"
)

print(
    "UnitPrice（單價）<= 0：",
    (clean_df["UnitPrice"] <= 0).sum(),
    "筆"
)

print(
    "Description（商品描述）缺失：",
    clean_df["Description"].isnull().sum(),
    "筆"
)

print(
    "CustomerID（顧客編號）缺失：",
    clean_df["CustomerID"].isnull().sum(),
    "筆"
)


# ------------------------------------------------------------
# 15. 儲存加入分析欄位後的資料
# ------------------------------------------------------------

clean_df.to_csv(
    "clean_online_retail_final.csv",
    index=False,
    encoding="utf-8-sig"
)

customer_df.to_csv(
    "customer_online_retail_final.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\n========== EDA（探索性資料分析）完成 ==========")