import logging
import random
import time
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

RETRYABLE_STATUS_CODES = {
    429,
    500,
    502,
    503,
    504,
}


def request_with_retry(
    url,
    max_retries=3,
    base_delay=0.5,
):

    for attempt in range(
        1,
        max_retries + 1,
    ):

        try:

            response = requests.get(
                url,
                timeout=(3, 10),
            )

            if response.status_code == 200:

                return response

            if (
                response.status_code
                not in RETRYABLE_STATUS_CODES
            ):
                response.raise_for_status()

            if attempt == max_retries:
                break

            if response.status_code == 429:

                retry_after = response.headers.get(
                    "Retry-After"
                )

                if retry_after:
                    wait_time = float(
                        retry_after
                    )
                    logging.info(
                        f"Rate limited. "
                        f"Using Retry-After: {wait_time}s"
                    )
                else:
                    wait_time = (
                        base_delay
                        * (
                            2
                            ** (attempt - 1)
                        )
                    )

            else:

                wait_time = (
                    base_delay
                    * (
                        2
                        ** (attempt - 1)
                    )
                )

            jitter = random.uniform(
                0,
                0.5,
            )

            sleep_time = (
                wait_time + jitter
            )

            logging.warning(
                f"Attempt {attempt} failed "
                f"with {response.status_code}. "
                f"Wait {sleep_time:.2f}s"
            )

            time.sleep(sleep_time)

        except requests.exceptions.RequestException as error:

            if attempt == max_retries:
                raise

            wait_time = (
                base_delay
                * (
                    2
                    ** (attempt - 1)
                )
            )

            jitter = random.uniform(
                0,
                0.5,
            )

            sleep_time = (
                wait_time + jitter
            )

            logging.warning(
                f"Network error: {error}. "
                f"Wait {sleep_time:.2f}s"
            )

            time.sleep(sleep_time)

    raise RuntimeError(
        "Maximum retries exceeded"
    )


requests.get(
    "http://127.0.0.1:8000/reset"
)

response = request_with_retry(
    "http://127.0.0.1:8000/unstable"
)

print(
    response.json()
)