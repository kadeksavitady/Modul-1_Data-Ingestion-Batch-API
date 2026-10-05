import requests

def fetch_pages(url, limit=10):
    MAX_PAGES = 1000  # Syarat 5: Memiliki MAX_PAGES
    page = 1
    
    while True:
        # Pengecekan batas maksimal halaman
        if page > MAX_PAGES:
            raise RuntimeError(f"Melebihi batas MAX_PAGES ({MAX_PAGES})")
            
        # Syarat 2: Menggunakan timeout
        response = requests.get(
            url,
            params={"page": page, "limit": limit},
            timeout=(3, 10)
        )
        
        # Syarat 3: Memanggil raise_for_status()
        response.raise_for_status()
        
        payload = response.json()
        data = payload.get("data", [])
        
        # Syarat 4: Berhenti jika data kosong
        if not data:
            print("Data kosong, menghentikan pengambilan data.")
            break
            
        # Syarat 1: Menggunakan generator
        yield data
        
        page += 1

# --- BLOK UNTUK MENGUJI FUNGSI ---
if __name__ == "__main__":
    api_url = "http://127.0.0.1:8000/transactions"
    
    total_data = 0
    # Mengambil data menggunakan generator
    for batch in fetch_pages(api_url, limit=10):
        print(f"Berhasil mengambil {len(batch)} record data.")
        total_data += len(batch)
        
    print(f"\nTotal keseluruhan: {total_data} record.")