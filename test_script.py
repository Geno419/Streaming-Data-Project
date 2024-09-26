import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import logging
from script import (
    get_user_input,
    validate_date,
    make_api_request,
    handle_response,
    upload_to_kinesis
)


class TestScript(unittest.TestCase):


    @patch("builtins.input", side_effect=["test query", ""])
    def test_get_user_input(self, mock_input):
        """
        Test for correct user input handling for search queries and dates.
        """
        user_query, date_from = get_user_input()
        self.assertEqual(user_query, "test query")
        self.assertEqual(date_from, "")


    def test_validate_date_valid(self):
        """
        Test that valid dates are correctly processed.
        """
        self.assertEqual(validate_date("2024-01-01"), ("2024-01-01", "newest"))


    def test_validate_date_invalid_format(self):
        """
        Test that invalid date formats prompt for new input.
        """
        with patch('builtins.input', side_effect=["invalid-date", "2024-01-01"]):
            self.assertEqual(validate_date("invalid-date"), ("2024-01-01", "newest"))


    @patch("builtins.input", return_value="")
    def test_validate_date_invalid(self, mock_input):
        """
        Test that invalid dates are handled and corrected by prompting for new input.
        """
        with patch('builtins.input', side_effect=["invalid-date", "2024-01-01"]):
            self.assertEqual(validate_date("invalid-date"), ("2024-01-01", "newest"))


    @patch("requests.get")
    def test_make_api_request(self, mock_get):
        """
        Test that the API request function correctly handles the response from the API.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"response": {"results": []}}

        response = make_api_request("test query", "2024-01-01", "oldest")
        self.assertEqual(response.status_code, 200)


    def test_handle_response(self):
        """
        Test that the API response handler correctly processes valid data.
        """
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "response": {
                "results": [
                    {
                        "webPublicationDate": "2024-01-01",
                        "webTitle": "Test Title",
                        "webUrl": "http://test.url",
                    }
                ]
            }
        }

        results = handle_response(mock_response)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["webTitle"], "Test Title")


    @patch("boto3.client")
    def test_upload_to_kinesis(self, mock_boto_client):
        """
        Test that the Kinesis client correctly uploads the JSON data.
        """
        mock_kinesis_client = mock_boto_client.return_value
        mock_kinesis_client.put_record.return_value = {
            "SequenceNumber": "123",
            "ShardId": "shardId-000000000000"
        }

        json_data = {
            "webTitle": "Test Title",
            "webPublicationDate": "2024-01-01",
            "webUrl": "http://test.url",
        }

        response = upload_to_kinesis(json_data, mock_kinesis_client, "test-stream")
        
        # Verify Kinesis put_record was called
        mock_kinesis_client.put_record.assert_called_once()
        self.assertEqual(response["SequenceNumber"], "123")

if __name__ == "__main__":
    unittest.main()
