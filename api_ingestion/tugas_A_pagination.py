def fetch_all(fetch_page):

    page = 1

    while True:

        response = fetch_page(
            page
        )

        data = response.get(
            "data",
            [],
        )

        if not data:
            break

        yield data

        page += 1