import json
from unittest.mock import patch

from forge_webhook_parser import load_json_data, parse_arguments


class TestParseArguments:
    def test_with_file_arg(self):
        with patch("sys.argv", ["script_name", "-f", "payload.json"]):
            args = parse_arguments()
            assert args.file == "payload.json"
            assert args.url is None

    def test_with_url_arg(self):
        with patch(
            "sys.argv", ["script_name", "-u", "http://example.com/payload.json"]
        ):
            args = parse_arguments()
            assert args.url == "http://example.com/payload.json"
            assert args.file is None


class TestLoadJsonDataFile:
    def test_load_from_file_github(self, mock_args_file, github_payload):
        with patch("builtins.open") as mock_open:
            mock_file = mock_open.return_value.__enter__.return_value
            mock_file.read.return_value = json.dumps(github_payload)

            data = load_json_data(mock_args_file)

            assert data == github_payload
            mock_open.assert_called_once_with("payload.json", "r", encoding="utf-8")

    def test_load_from_file_gitlab(self, mock_args_file, gitlab_payload):
        with patch("builtins.open") as mock_open:

            mock_file = mock_open.return_value.__enter__.return_value
            mock_file.read.return_value = json.dumps(gitlab_payload)

            data = load_json_data(mock_args_file)

            assert data == gitlab_payload
            mock_open.assert_called_once_with("payload.json", "r", encoding="utf-8")


class TestLoadJsonDataUrl:
    @patch("requests.get")
    def test_load_from_url_github(self, mock_get, mock_args_url, github_payload):

        mock_response = mock_get.return_value
        mock_response.json.return_value = github_payload

        data = load_json_data(mock_args_url)

        assert data == github_payload
        mock_get.assert_called_once_with("http://example.com/payload.json")

    @patch("requests.get")
    def test_load_from_url_gitlab(self, mock_get, mock_args_url, gitlab_payload):

        mock_response = mock_get.return_value
        mock_response.json.return_value = gitlab_payload

        data = load_json_data(mock_args_url)

        assert data == gitlab_payload
        mock_get.assert_called_once_with("http://example.com/payload.json")
