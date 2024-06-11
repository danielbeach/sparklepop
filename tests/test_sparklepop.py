import pytest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
import sparklepop

@pytest.fixture
def mock_boto_client(mocker):
    return mocker.patch('boto3.client')

def test_cw_free_disk_space_request(mock_boto_client):
    # Mock the CloudWatch client
    mock_client_instance = MagicMock()
    mock_boto_client.return_value = mock_client_instance

    # Define the mock response
    mock_response = {
        'MetricDataResults': [{
            'Values': [1000000000]
        }]
    }
    mock_client_instance.get_metric_data.return_value = mock_response

    # Instantiate SparklePop and call the method
    sparkle_pop = sparklepop.SparklePop('test-instance')
    result = sparkle_pop.cw_free_disk_space_request()

    # Assert the response
    assert result == [1000000000]

def test_convert_bytes_to_gb():
    bytes = 1073741824  # 1 GB in bytes
    expected_gb = 1

    # Call the static method
    result = sparklepop.SparklePop.convert_bytes_to_gb(bytes)

    # Assert the conversion
    assert result == expected_gb

@pytest.fixture
def sparkle_pop_instance(mock_boto_client):
    # Mock the CloudWatch client
    mock_client_instance = MagicMock()
    mock_boto_client.return_value = mock_client_instance

    # Define the mock response for get_metric_data
    mock_response = {
        'MetricDataResults': [{
            'Values': [1000000000]  # 1 GB in bytes
        }]
    }
    mock_client_instance.get_metric_data.return_value = mock_response

    return sparklepop.SparklePop('test-instance')

def test_get_free_disk_space(sparkle_pop_instance):
    # Call the method
    result = sparkle_pop_instance.get_free_disk_space()

    # Assert the result in GB
    assert result == 0.9313225746154785  # 1000000000 bytes converted to GB

def test_check_on_free_disk_space_below_threshold(sparkle_pop_instance):
    # Test the scenario where free disk space is below the threshold
    with pytest.raises(Exception, match="Free storage space is less than 10GB. Current free storage space is 0.9313225746154785GB"):
        sparkle_pop_instance.check_on_free_disk_space(minimum_gb=10)

def test_check_on_free_disk_space_above_threshold(sparkle_pop_instance, capsys):
    # Test the scenario where free disk space is above the threshold
    sparkle_pop_instance.check_on_free_disk_space(minimum_gb=0.5)
    
    # Capture the output
    captured = capsys.readouterr()

    # Assert the output
    assert "Free storage space is 0.9313225746154785GB. No action required." in captured.out
