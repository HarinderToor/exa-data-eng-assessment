import json
from unittest.mock import patch, MagicMock

from src.extractors import extract_resources


class TestEndToEndExtraction:
    @patch("src.extractors.extract_patients_from_bundle")
    @patch("src.extractors.extract_encounters_from_bundle")
    @patch("src.extractors.extract_observations_from_bundle")
    @patch("src.extractors.extract_conditions_from_bundle")
    def test_extract_and_persist_all_resources(
        self,
        mock_conditions,
        mock_observations,
        mock_encounters,
        mock_patients,
        fhir_bundle_file,
    ):
        mock_db = MagicMock()
        mock_patients.return_value = [MagicMock()]
        mock_encounters.return_value = [MagicMock()]
        mock_observations.return_value = [MagicMock()]
        mock_conditions.return_value = [MagicMock()]

        extract_resources(fhir_bundle_file, mock_db)

        assert mock_patients.called
        assert mock_encounters.called
        assert mock_observations.called
        assert mock_conditions.called
        assert mock_db.merge.call_count == 4
        assert mock_db.commit.called

    @patch("src.extractors.extract_patients_from_bundle")
    def test_extract_multiple_bundles(self, mock_patients, tmp_path):
        bundle1_path = tmp_path / "bundle1.json"
        bundle1_path.write_text(json.dumps({"entry": []}))
        bundle2_path = tmp_path / "bundle2.json"
        bundle2_path.write_text(json.dumps({"entry": []}))

        mock_db = MagicMock()
        mock_patients.return_value = []

        extract_resources(str(bundle1_path), mock_db)
        extract_resources(str(bundle2_path), mock_db)

        assert mock_patients.call_count == 2
        assert mock_db.commit.call_count == 2

    @patch("src.extractors.extract_patients_from_bundle")
    def test_merge_duplicate_resources(self, mock_patients, tmp_path):
        bundle_path = tmp_path / "bundle.json"
        bundle_path.write_text(json.dumps({"entry": []}))

        mock_db = MagicMock()
        mock_patient = MagicMock()
        mock_patients.return_value = [mock_patient]

        extract_resources(str(bundle_path), mock_db)
        extract_resources(str(bundle_path), mock_db)

        assert mock_db.merge.call_count == 2
        assert mock_db.commit.call_count == 2
