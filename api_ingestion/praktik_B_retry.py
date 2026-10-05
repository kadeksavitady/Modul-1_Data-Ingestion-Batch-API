import requests
import time
import random

def get_with_retry(url):
    max_retries = 3
    timeout = (3, 10) # 3 detik connect, 10 detik read
    base_delay = 1
    retryable_statuses = {500, 502, 503, 504}

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status() # Cek apakah ada error HTTP
            return response.json()

        except requests.exceptions.HTTPError as e:
            status = e.response.status_code
            
            # Jika error bersifat client-side (seperti 400, 401, 403, 404), langsung hentikan
            if status not in retryable_statuses:
                raise 
                
            # Jika mencapai batas maksimum percobaan, lempar errornya
            if attempt == max_retries:
                raise

        except requests.exceptions.RequestException:
            # Menangkap error jaringan seperti ConnectionError atau Timeout
            if attempt == max_retries:
                raise

        # Kalkulasi Exponential Backoff + Jitter
        sleep_time = (base_delay * (2 ** (attempt - 1))) + random.uniform(0, 1)
        time.sleep(sleep_time)