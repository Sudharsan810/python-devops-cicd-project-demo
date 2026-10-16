from click.testing import CliRunner
from pytest_mock import MockerFixture

from simple_http_checker.cli import main


def test_cli_no_urls():
    runner = CliRunner()
    result = runner.invoke(main, [])

    assert result.exit_code == 0
    assert "Usage: check-urls" in result.output


def test_cli_single_url_success(mocker: MockerFixture):
    url = "https://www.example.com"

    mock_request_get = mocker.patch("simple_http_checker.cli.check_urls")
    mock_request_get.return_value = {url: "200 OK"}
    runner = CliRunner()
    result = runner.invoke(main, [url])

    assert result.exit_code == 0
    assert "200 OK" in result.output
    mock_request_get.assert_called_once_with((url,), 5)


def test_cli_single_url_timeout(mocker: MockerFixture):
    url = "https://www.example.com"

    mock_request_get = mocker.patch("simple_http_checker.cli.check_urls")
    mock_request_get.return_value = {url: "200 OK"}
    runner = CliRunner()
    result = runner.invoke(main, [url, "--timeout", "10"])

    assert result.exit_code == 0
    assert "200 OK" in result.output
    mock_request_get.assert_called_once_with((url,), 10)
