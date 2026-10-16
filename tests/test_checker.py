import pytest
import requests
from pytest_mock import MockerFixture

from simple_http_checker.checker import check_urls


def test_check_urls_success(mocker: MockerFixture):
    mock_request_get = mocker.patch("simple_http_checker.checker.requests.get")

    mock_response = mocker.MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.reason = "OK"
    mock_response.ok = True
    mock_request_get.return_value = mock_response

    urls = ["www.example.com"]
    result = check_urls(urls)
    mock_request_get.assert_called_once_with(urls[0], timeout=5)
    assert result[urls[0]] == "200 OK"


def test_check_urls_client_error(mocker: MockerFixture):
    mock_request_get = mocker.patch("simple_http_checker.checker.requests.get")

    mock_response = mocker.MagicMock(spec=requests.Response)
    mock_response.status_code = 404
    mock_response.reason = "NOT FOUND"
    mock_response.ok = False
    mock_request_get.return_value = mock_response

    urls = ["www.example.com/nonexistance"]
    result = check_urls(urls)
    mock_request_get.assert_called_once_with(urls[0], timeout=5)
    assert result[urls[0]] == "404 NOT FOUND"


@pytest.mark.parametrize(
    "error_exception, expected_status",
    [
        (requests.exceptions.Timeout, "TIMEOUT"),
        (requests.exceptions.ConnectionError, "CONNECTION_ERROR"),
        (requests.exceptions.RequestException, "REQUEST_ERROR: RequestException"),
    ],
)
def test_check_urls_request_exceptions(
    mocker: MockerFixture,
    error_exception: type[requests.exceptions.RequestException],
    expected_status: str,
):
    mock_request_get = mocker.patch("simple_http_checker.checker.requests.get")
    mock_request_get.side_effect = error_exception(f"stimulated {expected_status}")

    urls = ["www.somesite.com"]
    result = check_urls(urls)

    mock_request_get.assert_called_once_with(urls[0], timeout=5)
    assert result[urls[0]] == expected_status


def test_check_urls_with_multiple_urls(mocker: MockerFixture):
    mock_request_get = mocker.patch("simple_http_checker.checker.requests.get")

    mock_response_ok = mocker.MagicMock(spec=requests.Response)
    mock_response_ok.status_code = 200
    mock_response_ok.reason = "OK"
    mock_response_ok.ok = True

    timeout_exception = requests.exceptions.Timeout("stimulated TIMEOUT")

    mock_response_fail = mocker.MagicMock(spec=requests.Response)
    mock_response_fail.status_code = 500
    mock_response_fail.reason = "Server Error"
    mock_response_fail.ok = False

    mock_request_get.side_effect = [
        mock_response_ok,
        timeout_exception,
        mock_response_fail,
    ]

    urls = [
        "https://success.com",
        "https://timeout.com",
        "https://servererror.com",
    ]
    result = check_urls(urls)
    assert len(result) == 3
    assert mock_request_get.call_count == 3
    assert result["https://success.com"] == "200 OK"
    assert result["https://timeout.com"] == "TIMEOUT"
    assert result["https://servererror.com"] == "500 Server Error"


def test_check_urls_empty_list():
    result = check_urls([])
    assert result == {}


def test_check_urls_custom_timeout(mocker: MockerFixture):
    mock_request_get = mocker.patch("simple_http_checker.checker.requests.get")

    mock_response = mocker.MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.reason = "OK"
    mock_response.ok = True
    mock_request_get.return_value = mock_response

    urls = ["www.example.com"]
    custom_timeout = 10
    result = check_urls(urls, timeout=custom_timeout)
    mock_request_get.assert_called_once_with(urls[0], timeout=custom_timeout)
    assert result[urls[0]] == "200 OK"
