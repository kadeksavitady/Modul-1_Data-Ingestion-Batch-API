from pathlib import Path
import pandas as pd
from storage import save_records

# 1. Generate dataset yang agak besar (misal 100.000 baris) agar kompresi terasa
print("Membuat dataset dummy...")
records = [
    {
        "id": i,
        "customer": f"customer_{i % 1000}",
        "amount": i * 150,
        "updated_at": "2026-09-01T08:00:00+00:00"
    }
    for i in range(100000)
]

# Pastikan direktori data ada
Path("data").mkdir(parents=True, exist_ok=True)

# 2. Uji dengan kompresi SNAPPY
file_snappy = "data/transactions_snappy.parquet"
print(f"Menyimpan dengan kompresi 'snappy' ke {file_snappy}...")
# Memodifikasi pemanggilan dengan parameter compression
path_snappy = Path(file_snappy)
path_snappy.parent.mkdir(parents=True, exist_ok=True)
pd.DataFrame(records).to_parquet(path_snappy, index=False, compression="snappy")

# 3. Uji dengan kompresi GZIP
file_gzip = "data/transactions_gzip.parquet"
print(f"Menyimpan dengan kompresi 'gzip' ke {file_gzip}...")
path_gzip = Path(file_gzip)
path_gzip.parent.mkdir(parents=True, exist_ok=True)
pd.DataFrame(records).to_parquet(path_gzip, index=False, compression="gzip")

# 4. Tampilkan perbandingan ukuran file (dalam ukuran KB / MB)
size_snappy = Path(file_snappy).stat().st_size / 1024
size_gzip = Path(file_gzip).stat().st_size / 1024

print("\n" + "="*30)
print("HASIL EKSPERIMEN KOMPRESI")
print("="*30)
print(f"Ukuran file Snappy : {size_snappy:.2f} KB")
print(f"Ukuran file Gzip   : {size_gzip:.2f} KB")
print("="*30)