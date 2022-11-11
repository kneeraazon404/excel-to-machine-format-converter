import pandas as pd
import string
import random
from datetime import datetime


def generate_machine_data(
    file_path,
    market_id,
    store_number,
    cash_register_number,
):
    df = pd.read_excel(
        file_path,
        skiprows=5,
    )

    # Combine Date and Time columns into a single column DateTime
    date_time = []
    for i in range(0, len(df) - 1):
        date_time.append(
            df["Date"][i].strftime("%Y%d%m") + df["Time"][i].strftime("%H%M%S")
        )
    # print(DateTime)
    df["DateTime"] = pd.Series(date_time)

    # Random string generator for digits
    def ran_gen(size, chars=string.digits):
        return "".join(random.choice(chars) for x in range(size))

    # merket id generation

    ids = []

    for i in range(0, len(df)):
        ids.append(str(market_id))
    df["Market ID"] = ids

    store_numbers = []
    for i in range(0, len(df)):
        store_numbers.append(str(store_number))
    df["Store ID"] = store_numbers

    # Cash Register ID/ Terminal ID generation
    cr_ids = []
    for i in range(0, len(df)):
        cr_ids.append(str(cash_register_number))
    df["CR ID"] = cr_ids

    print(df[df["Receipt #"].isnull()])

    df["Receipt #"] = pd.to_numeric(df["Receipt #"], errors="coerce")
    df = df.dropna(subset=["Receipt #"])
    df["Receipt #"] = df["Receipt #"].astype(int)
    for i in range(0, len(df)):
        df["Receipt #"][i] = str(df["Receipt #"][i]).zfill(11)

    seq_nums = []
    for i in range(1, len(df) + 1):
        seq_nums.append(i)
    df["Sequence #"] = seq_nums
    for i in range(0, len(df)):
        df["Sequence #"][i] = str(df["Sequence #"][i]).zfill(5)

    # Transaction Type
    df["Transaction Type"] = "Sale"
    for i in range(0, len(df)):
        if df["Transaction Type"][i] == "Sale":
            df["Transaction Type"][i] = "S"
        elif df["Transaction Type"][i] == "Return":
            df["Transaction Type"][i] = "R"
        elif df["Transaction Type"][i] == "No-Sale":
            df["Transaction Type"][i] = "N"
        else:
            df["Transaction Type"][i] = "X"

    # Article
    articles = []
    for i in range(0, len(df)):
        articles.append(ran_gen(8, "0123456789"))
    df["Article"] = articles

    for i in range(0, len(df)):
        df["Article"][i] = str(df["Article"][i]).zfill(12)

    # Quantity Sold

    for i in range(0, len(df)):
        df["Qty Sold"][i] = str(df["Qty Sold"][i]) + "0000"
        df["Qty Sold"][i] = str(df["Qty Sold"][i]).zfill(12)
    # Store Local Currency
    store_l_currency = []
    for i in range(0, len(df)):
        store_l_currency.append(ran_gen(3, "0123456789"))
    df["Store LC"] = store_l_currency
    for i in range(0, len(df)):
        df["Store LC"][i] = str(df["Store LC"][i]) + "0000"
        df["Store LC"][i] = str(df["Store LC"][i]).zfill(20)
    # Franchise Local Currency
    franch_currency = []
    for i in range(0, len(df)):
        franch_currency.append(ran_gen(3, "0123456789"))
    df["Franchise LC"] = franch_currency
    for i in range(0, len(df)):
        df["Franchise LC"][i] = str(df["Franchise LC"][i]) + "0000"
        df["Franchise LC"][i] = str(df["Franchise LC"][i]).zfill(20)
    df = df.rename(columns={"Market ID": "MarketID", "CR ID": "CRID"})

    df["All"] = (
        df["MarketID"]
        + "|"
        + df["Store ID"]
        + "|"
        + +df["DateTime"]
        + "|"
        + df["CRID"]
        + "|"
        + df["Receipt #"]
        + "|"
        + df["Sequence #"]
        + "|"
        + df["Transaction Type"]
        + "|"
        + df["Article"]
        + "|"
        + df["Qty Sold"]
        + "|"
        + df["Store LC"]
        + "|"
        + df["Franchise LC"]
    )
    # print(df["Receipt #"])
    today = datetime.today().strftime("%Y%m%d%H")
    f = f"{today}.SALES.{df['MarketID'][0]}"

    file = df["All"].to_csv(f, header=None, index=None, mode="a")
    print(file)
    return file
