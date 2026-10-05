import os
from pathlib import Path
import pandas as pd
import requests
from watermark import load_watermark, save_watermark

FILE_PATH = "state/watermark.json"
API_URL = "http://127.0.0.1:8000/transactions"
PARQUET_DIR = Path("data/transactions")

def fetch_and_process(is_run_first=False):
    # 1. Read Watermark
    watermark_before = load_watermark(FILE_PATH)
    print(f"Watermark before: {watermark_before}")

    # 2. Request API dengan parameter updated_since
    params = {
        "page": 1,
        "limit": 100,
        "updated_since": watermark_before,
    }
    
    response = requests.get(API_URL, params=params, timeout=(3, 10))
    response.raise_for_status()
    
    payload = response.json()
    records = payload.get("data", [])
    
    records_fetched = len(records)
    print(f"Records fetched: {records_fetched}")

    if records_fetched > 0:
        # 3. Process & Write Storage (Simpan ke Parquet)
        PARQUET_DIR.mkdir(parents=True, exist_ok=True)
        df = pd.DataFrame(records)
        
        # Simpan dengan nama unik (misal berdasarkan timestamp atau increment file)
        file_name = f"transactions_{'initial' if is_run_first else 'incremental'}.parquet"
        file_dest = PARQUET_DIR / file_name
        df.to_parquet(file_dest, index=False)
        print(f"Data saved to {file_dest}")

        # 4. Menentukan Watermark Baru (Bagian 12.9)
        new_watermark = max(record["updated_at"] for record in records)
        
        # 5. Update Watermark (Dilakukan PALING AKHIR setelah sukses simpan)
        save_watermark(FILE_PATH, new_watermark)

    watermark_after = load_watermark(FILE_PATH)
    print(f"Watermark after: {watermark_after}")
    print("-" * 40)

if __name__ == "__main__":
    # Simulasi Run 1 (Hapus watermark.json dulu jika ingin simulasi dari awal)
    print("=== MENJALANKAN RUN 1 (Initial Load) ===")
    # Jika ingin reset total untuk Run 1, uncomment baris bawah:
    # if Path(FILE_PATH).exists(): Path(FILE_PATH).unlink()
    
    fetch_and_process(is_run_first=True)

    # Simulasi Run 2 (Incremental Load - jalankan lagi setelah ada data baru di API)
    print("\n=== MENJALANKAN RUN 2 (Incremental Load) ===")
    fetch_and_process(is_run_first=False)