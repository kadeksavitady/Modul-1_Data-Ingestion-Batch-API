import time
import requests


url = (
    "http://127.0.0.1:8000/"
    "unstable"
)

MAX_RETRIES = 5
BASE_DELAY = 1


for attempt in range(
    1,
    MAX_RETRIES + 1,
):

    response = requests.get(
        url,
        timeout=(3, 10),
    )

    if response.status_code == 200:

        print(
            "Success:",
            response.json(),
        )

        break

    if response.status_code in (
        500,
        502,
        503,
        504,
    ):

        if attempt == MAX_RETRIES:
            break

        import random


        wait_time = (
            BASE_DELAY
            * (2 ** (attempt - 1))
        )

        jitter = random.uniform(
            0,
            1,
        )

        sleep_time = (
            wait_time + jitter
        )

        continue

    response.raise_for_status()

else:

    raise RuntimeError(
        "Maximum retries exceeded"
    )