from pathlib import Path
import pandas as pd

def save_records(
    records,
    output_file,
):
    path = Path(output_file)
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    df = pd.DataFrame(
        records
    )
    df.to_parquet(
        path,
        index=False,
        compression="snappy",
    )
    return path

def read_records(
    input_file,
):
    return pd.read_parquet(
        input_file
    )

if __name__ == "__main__":
    # Kode pengujian hanya jalan jika "python storage.py" dieksekusi
    records = [
        {
            "id": 1,
            "customer": "Andi",
            "amount": 10000,
            "updated_at": "2026-09-01T08:00:00+00:00",
        },
        {
            "id": 2,
            "customer": "Budi",
            "amount": 20000,
            "updated_at": "2026-09-01T09:00:00+00:00",
        },
    ]
    
    output_file = "data/transactions.parquet"
    save_records(records, output_file)
    print("Parquet saved")
    
    df = read_records(output_file)
    print(df)
    
    print("Parquet validation passed")