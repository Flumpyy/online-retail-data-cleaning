import pandas as pd

df = pd.read_excel("data/Online Retail.xlsx")

print(df.head())
print("讀取成功")
print(df.shape)
print("\n欄位名稱")
print(df.columns)

print("\n資料型態")
print(df.dtypes)

print("\n缺失值數量：")
print(df.isnull().sum())

print("\n完全重複的資料筆數：")
print(df.duplicated().sum())

print("\n重複資料範例：")
print(df[df.duplicated(keep=False)].head(20))

pd.set_option("display.max_columns", None)

print("\n重複資料完整內容：")
print(df[df.duplicated(keep=False)].head(20))


print("\n重複資料數量：")
print(df.duplicated().sum())

print("\n重複資料的 Quantity 分布：")
print(df[df.duplicated(keep=False)]["Quantity"].value_counts().head(20))

print("\n數值欄位基本統計：")
print(df.describe())

print("\nQuantity 最大的資料：")
print(df.nlargest(10, "Quantity"))

print("\nQuantity 最小的資料：")
print(df.nsmallest(10, "Quantity"))

print("\nInvoiceNo 以 C 開頭的資料：")
print(df[df["InvoiceNo"].astype(str).str.startswith("C")].head(20))

cancelled = df[df["InvoiceNo"].astype(str).str.startswith("C")]

print("\n取消交易筆數：")
print(len(cancelled))

print("\n取消交易 Quantity 統計：")
print(cancelled["Quantity"].describe())

print("\n取消交易中 Quantity >= 0 的筆數：")
print((cancelled["Quantity"] >= 0).sum())

print("\nUnitPrice 基本統計：")
print(df["UnitPrice"].describe())

print("\nUnitPrice = 0 的筆數：")
print((df["UnitPrice"] == 0).sum())

print("\nUnitPrice < 0 的筆數：")
print((df["UnitPrice"] < 0).sum())

print("\nUnitPrice < 0 的完整資料：")
print(df[df["UnitPrice"] < 0])

print("\nUnitPrice = 0 的資料範例：")
print(df[df["UnitPrice"] == 0].head(30))

zero_price = df[df["UnitPrice"] == 0]

print("\nUnitPrice = 0 的總筆數：")
print(len(zero_price))

print("\nUnitPrice = 0 資料的缺失值數量：")
print(zero_price.isnull().sum())

print("\nUnitPrice = 0 且有 CustomerID 的資料：")
print(zero_price[zero_price["CustomerID"].notnull()])

print("\nUnitPrice = 0 最常見的 Description：")
print(zero_price["Description"].value_counts(dropna=False).head(20))

print("\nUnitPrice = 0 且有 CustomerID 的筆數：")
print(zero_price["CustomerID"].notnull().sum())

print("\nUnitPrice = 0 且沒有 CustomerID 的筆數：")
print(zero_price["CustomerID"].isnull().sum())

zero_price_customer = zero_price[
    zero_price["CustomerID"].notnull()
]

print("\n0 元且有 CustomerID 的 Description：")
print(zero_price_customer["Description"].value_counts(dropna=False))

print("\n最常見的 StockCode：")
print(df["StockCode"].value_counts().head(30))

print("\nStockCode = POST 的資料：")
print(df[df["StockCode"] == "POST"].head(20))

print("\n純英文字母的 StockCode：")

letter_codes = df[
    df["StockCode"].astype(str).str.fullmatch(r"[A-Za-z]+")
]

print(
    letter_codes[["StockCode", "Description"]]
    .value_counts()
)

print("\n特殊 StockCode 統計：")

special_summary = (
    letter_codes
    .groupby(["StockCode", "Description"])
    .agg(
        筆數=("StockCode", "size"),
        Quantity平均=("Quantity", "mean"),
        UnitPrice平均=("UnitPrice", "mean"),
        UnitPrice最小=("UnitPrice", "min"),
        UnitPrice最大=("UnitPrice", "max")
    )
)

print(special_summary)

print("\nInvoiceNo 格式統計：")

invoice_str = df["InvoiceNo"].astype(str)

print("C 開頭：", invoice_str.str.startswith("C").sum())
print("純數字：", invoice_str.str.fullmatch(r"\d+").sum())
print("其他格式：", (
    ~invoice_str.str.startswith("C")
    & ~invoice_str.str.fullmatch(r"\d+")
).sum())

other_invoice = df[
    ~invoice_str.str.startswith("C")
    & ~invoice_str.str.fullmatch(r"\d+")
]

print("\n其他格式 InvoiceNo 的完整資料：")
print(other_invoice)

