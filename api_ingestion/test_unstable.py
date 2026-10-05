import requests

# 1. Reset kondisi server agar hitungannya kembali dari awal
print("--- Mereset Server ---")
requests.get("http://127.0.0.1:8000/reset")
print("Server di-reset.")

# 2. Menembak endpoint unstable sebanyak 3 kali berturut-turut
url_unstable = "http://127.0.0.1:8000/unstable"

for i in range(1, 4):
    print(f"\nMengirim Request ke-{i}...")
    response = requests.get(url_unstable)
    print(f"Status Code: {response.status_code}")