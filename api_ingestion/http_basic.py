import requests


url = (
    "http://127.0.0.1:8000/not-found"
)

response = requests.get(
    url,
    timeout=(3, 10),
)

print("Status Code:")
print(response.status_code)

print("\nHeaders:")
print(dict(response.headers))

print("\nJSON Body:")
print(response.json())

print("\nRaise for Status:")
print(response.raise_for_status())
