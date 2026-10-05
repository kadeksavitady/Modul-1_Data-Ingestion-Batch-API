import requests

def fetch_pages(fetch_function, watermark, page_size=10):
    """
    Iterator halaman dengan incremental fetching.

    Args:
        fetch_function: fungsi yang memanggil API dan mengembalikan JSON payload
        watermark: nilai updated_since terakhir (string atau None)
        page_size: jumlah record per halaman

    Yields:
        List berisi record untuk setiap halaman yang berhasil diambil
    """
    page = 1

    while True:
        print(f"Fetching page {page} with watermark={watermark}")

        try:
            payload = fetch_function(page, page_size, watermark)
            data = payload.get("data", [])

            if not data:
                print("No more data (empty list)")
                break

            yield data
            print(f"Page {page}: {len(data)} record")

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print("Rate limit hit — need to implement retry logic")
                break
            raise

        page += 1