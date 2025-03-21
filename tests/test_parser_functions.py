import json
from unittest.mock import MagicMock, mock_open, patch

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


class TestLoadJsonData:
    @patch("builtins.open", new_callable=mock_open)
    def test_load_from_file_github(self, mock_file, github_payload):

        mock_file.return_value.__enter__.return_value.read.return_value = json.dumps(
            github_payload
        )

        args = MagicMock()
        args.file = "payload.json"
        args.url = None

        data = load_json_data(args)

        assert data == github_payload
        mock_file.assert_called_once_with("payload.json", "r", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open)
    def test_load_from_file_gitlab(self, mock_file, gitlab_payload):

        mock_file.return_value.__enter__.return_value.read.return_value = json.dumps(
            gitlab_payload
        )

        args = MagicMock()
        args.file = "payload.json"
        args.url = None

        data = load_json_data(args)

        assert data == gitlab_payload
        mock_file.assert_called_once_with("payload.json", "r", encoding="utf-8")
