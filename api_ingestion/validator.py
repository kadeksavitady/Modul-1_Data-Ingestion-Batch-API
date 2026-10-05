REQUIRED_FIELDS = {
    "id",
    "customer",
    "amount",
    "updated_at",
}


def validate_record(
    record,
):

    missing_fields = (
        REQUIRED_FIELDS
        - set(record.keys())
    )

    if missing_fields:

        raise ValueError(
            "Missing fields: "
            f"{sorted(missing_fields)}"
        )

    if not isinstance(
        record["id"],
        int,
    ):
        raise ValueError(
            "id must be int"
        )

    if not isinstance(
        record["customer"],
        str,
    ):
        raise ValueError(
            "customer must be str"
        )

    if not isinstance(
        record["amount"],
        (int, float),
    ):
        raise ValueError(
            "amount must be numeric"
        )


def validate_records(
    records,
):

    if not isinstance(
        records,
        list,
    ):
        raise ValueError(
            "records must be a list"
        )

    for record in records:
        validate_record(record)

    return True


if __name__ == "__main__":
    records = [
        {
            "id": 1,
            "customer": "customer_001",
            "amount": 10000,
            "updated_at": "2026-09-01T08:10:00+00:00",
        }
    ]

    validate_records(records)
    print("Validation passed")

def validate_unique_ids(
    records,
):

    ids = [
        record["id"]
        for record in records
    ]

    if len(ids) != len(set(ids)):
        raise ValueError(
            "Duplicate id detected"
        )