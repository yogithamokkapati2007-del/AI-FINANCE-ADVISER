import requests

BASE_URL = "http://127.0.0.1:5000"


def test_server():
    response = requests.get(f"{BASE_URL}/api/test")

    print("Status:", response.status_code)
    print("Response:", response.json())


if __name__ == "__main__":
    test_server()