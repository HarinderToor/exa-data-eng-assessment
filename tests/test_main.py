import json
from unittest.mock import patch, MagicMock

from src.main import main


class TestMain:
    @patch("src.main.extract_resources")
    @patch("src.main.SessionLocal")
    def test_main_processes_json_files(
        self, mock_session_local, mock_extract, tmp_path, monkeypatch
    ):
        (tmp_path / "file1.json").write_text(json.dumps({"entry": []}))
        (tmp_path / "file2.json").write_text(json.dumps({"entry": []}))
        (tmp_path / "ignore.txt").write_text("not json")

        mock_session = MagicMock()
        mock_session_local.return_value.__enter__.return_value = mock_session
        monkeypatch.setattr("src.main.DATA_DIR", str(tmp_path))

        with patch("sys.argv", ["main.py", "--data", str(tmp_path)]):
            main()

        assert mock_extract.call_count == 2
        assert mock_session.commit.call_count == 2

    @patch("src.main.extract_resources")
    @patch("src.main.SessionLocal")
    def test_main_handles_extraction_errors(
        self, mock_session_local, mock_extract, tmp_path, monkeypatch
    ):
        (tmp_path / "bad.json").write_text(json.dumps({"entry": []}))

        mock_session = MagicMock()
        mock_session_local.return_value.__enter__.return_value = mock_session
        mock_extract.side_effect = Exception("Extraction failed")
        monkeypatch.setattr("src.main.DATA_DIR", str(tmp_path))

        with patch("sys.argv", ["main.py", "--data", str(tmp_path)]):
            main()

        assert mock_session.rollback.called

    @patch("src.main.logging")
    def test_main_warns_when_no_files_found(self, mock_logging, tmp_path, monkeypatch):
        monkeypatch.setattr("src.main.DATA_DIR", str(tmp_path))

        with patch("sys.argv", ["main.py", "--data", str(tmp_path)]):
            main()

        assert mock_logging.warning.called

    @patch("src.main.extract_resources")
    @patch("src.main.SessionLocal")
    def test_main_accepts_custom_data_directory(
        self, mock_session_local, mock_extract, tmp_path, monkeypatch
    ):
        (tmp_path / "test.json").write_text(json.dumps({"entry": []}))

        mock_session = MagicMock()
        mock_session_local.return_value.__enter__.return_value = mock_session
        monkeypatch.setattr("src.main.DATA_DIR", str(tmp_path))

        with patch("sys.argv", ["main.py", "--data", str(tmp_path)]):
            main()

        assert mock_extract.called
