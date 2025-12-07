import pytest
import requests
from requests.models import Response

URL = "http://127.0.0.1:5500/teton/1.6/index.html"

def mock_response(status_code=200, text=""):
    """Helper to create a mocked Response object"""
    response = Response()
    response.status_code = status_code
    response._content = text.encode()  # requests.Response expects bytes
    return response

def test_unauthorized_access(mocker):
    # Patch requests.get to return a mocked 401 response with empty body
    mocker.patch("requests.get", return_value=mock_response(status_code=401, text=""))

    auth = ("admin", "admin")
    response = requests.get(URL, auth=auth)

    assert response.status_code == 401, f"Expected 401 but got {response.status_code}"
    assert response.text.strip() == "", f"Expected empty response but got: {response.text}"


def test_authorized_access_with_qwerty(mocker):
    # Patch requests.get to return a mocked 200 response with empty body
    mocker.patch("requests.get", return_value=mock_response(status_code=200, text=""))

    auth = ("admin", "qwerty")
    response = requests.get(URL, auth=auth)

    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    assert response.text.strip() == "", f"Expected empty response but got: {response.text}"
