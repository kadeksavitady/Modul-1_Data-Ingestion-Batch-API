import pandas as pd


data = [
    {
        "id": 1,
        "name": "Andi",
        "amount": 10000,
    },
    {
        "id": 2,
        "name": "Budi",
        "amount": 20000,
    },
]

df = pd.DataFrame(
    data
)

df.to_parquet(
    "data.parquet",
    index=False,
)

result = pd.read_parquet(
    "data.parquet"
)

print(result)