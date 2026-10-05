import time
import requests

url = "http://127.0.0.1:8000/rate-limited"
MAX_RETRIES = 5  # Syarat 4: Berhenti setelah maksimal 5 percobaan

# Menggunakan range(1, MAX_RETRIES + 1) agar hitungan dimulai dari 1 sampai 5
for attempt in range(1, MAX_RETRIES + 1):
    
    # Syarat 1: Menampilkan nomor percobaan
    print(f"\n--- Mengirim Request (Percobaan ke-{attempt}) ---")
    
    response = requests.get(
        url,
        timeout=(3, 10),
    )
    
    # Syarat 2: Menampilkan status code
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        print("Success:", response.json())
        break  # Keluar dari perulangan jika berhasil

    if response.status_code == 429:
        # Syarat 3: Membaca Retry-After
        retry_after = response.headers.get("Retry-After", "1")
        wait_time = float(retry_after)
        
        # Syarat 5: Menulis log setiap kali terjadi 429
        print(f"[LOG] Rate limit tercapai. Harus menunggu {wait_time} detik sebelum mencoba lagi.")
        
        time.sleep(wait_time)
        continue

    # Lemparkan error jika status code bukan 200 dan bukan 429
    response.raise_for_status()

# Blok ini hanya dieksekusi jika perulangan selesai tanpa pernah menemui 'break'
else:
    raise RuntimeError(f"Gagal mendapatkan data setelah {MAX_RETRIES} percobaan.")