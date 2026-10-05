"""
api_client.py — Fungsi HTTP request dengan retry, exponential backoff, jitter,
                dan penanganan rate limit (429).
"""

import time
import random
import logging
import requests

import config

logger = logging.getLogger(__name__)

import time
import requests
import logging

logger = logging.getLogger(__name__)

def get_json(session, url, params, timeout, max_retries, base_delay):
    for attempt in range(1, max_retries + 1):
        try:
            # Perbaikan: gunakan session.get dan parameter timeout bawaan fungsi
            response = session.get(url, params=params, timeout=timeout)
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.warning("Attempt %s failed: %s", attempt, e)
            if attempt == max_retries:
                logger.error("Max retries reached. Failed to fetch %s", url)
                raise
                
            sleep_time = base_delay * (2 ** (attempt - 1))
            logger.info("Waiting %s seconds before retry...", sleep_time)
            time.sleep(sleep_time)

    for attempt in range(1, config.MAX_RETRIES + 1):
        logger.debug(f"Request attempt {attempt}/{config.MAX_RETRIES} | url={url} | params={params}")

        try:
            response = requests.get(url, params=params, timeout=config.TIMEOUT)

            # ── 429: Rate Limit ────────────────────────────────────
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", config.DEFAULT_RETRY_AFTER))
                logger.warning(f"429 Rate Limit. Tunggu {retry_after} detik...")
                time.sleep(retry_after)
                continue

            # ── 5xx: Server Error → backoff + jitter ──────────────
            if response.status_code >= 500:
                if attempt == config.MAX_RETRIES:
                    logger.error(f"Server error {response.status_code} setelah {attempt} percobaan.")
                    response.raise_for_status()

                # Exponential backoff: 2^attempt detik, ditambah jitter acak
                wait = min(config.BACKOFF_BASE ** attempt, config.BACKOFF_MAX)
                jitter = random.uniform(0, wait * 0.3)
                total_wait = round(wait + jitter, 2)
                logger.warning(
                    f"Server error {response.status_code}. "
                    f"Retry ke-{attempt} dalam {total_wait}s (backoff={wait}s, jitter={round(jitter,2)}s)..."
                )
                time.sleep(total_wait)
                continue

            # ── Respons sukses ─────────────────────────────────────
            response.raise_for_status()
            logger.debug(f"Respons OK ({response.status_code})")
            return response.json()

        except requests.exceptions.Timeout:
            logger.warning(f"Timeout pada attempt {attempt}. Mencoba lagi...")
            if attempt == config.MAX_RETRIES:
                raise

        except requests.exceptions.ConnectionError:
            logger.error("Gagal konek ke server. Pastikan mock_api.py sudah berjalan.")
            raise

    raise Exception(f"Semua {config.MAX_RETRIES} percobaan gagal untuk URL: {url}")
