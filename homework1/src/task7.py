import requests


def get_json(url):
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    data = get_json("https://jsonplaceholder.typicode.com/todos/1")
    print(data)