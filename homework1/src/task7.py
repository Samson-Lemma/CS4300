"""Task 7: Demonstrate use of the requests package."""

import requests


def get_json(url):
    """Request JSON data from a URL and return the parsed response."""
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    data = get_json("https://jsonplaceholder.typicode.com/todos/1")
    print(data)