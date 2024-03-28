from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import pytest
from appserver.main import app, get_db
from appserver.models import Claim

client = TestClient(app)

@pytest.fixture
def mock_db_session():
    with patch('appserver.main.get_db', new_callable=Mock) as mock_db:
        mock_session = Mock()
        mock_db.return_value = mock_session
        yield mock_session


# test point retrieval
def test_single_claim_retrieval(mock_db_session):
    claim_dict = {
        "u_id": "wfM6lT5V3h",
        "created_at": "2024-03-29T00:39:33.838136",
        "service_date": "2018-03-28T00:00:00",
        "submitted_procedure": "D0181",
        "quadrant": "",
        "plan_group": "GRP-1001",
        "subscriber_id": 3730182532,
        "provider_npi": 1497775520,
        "provider_fees": "$300.0",
        "allowed_fees": "$100.0",
        "member_coinsurance": "$10.0",
        "member_copay": "$20.0"
    }
    test_claim = Claim(**claim_dict)
    mock_db_session.get.return_value = test_claim

    response = client.get('/claim/get/wfM6lT5V3h')

    assert response.status_code == 200
    assert response.json()['claim'] == claim_dict


# test point retrival failure
def test_single_claim_retreival_fail(mock_db_session):
    mock_db_session.get.return_value = None

    response = client.get('/claim/get/wfM6lT5V3hasf')

    assert response.status_code == 404


# test invalid insertion
def test_invalid_insertion(mock_db_session):
    claim_dict = {
        "u_id": "wfM6lT5V3h",
        "service_date": "3/28/18 0:00",
        "submitted_procedure": "0181",
        "quadrant": "",
        "plan_group": "GRP-1001",
        "subscriber_id": 3730182532,
        "provider_npi": 1497775520,
        "provider_fees": "$300.0",
        "allowed_fees": "$100.0",
        "member_coinsurance": "$10.0",
        "member_copay": "$20.0"
    }

    try:
        response = client.post('/claim/add', json=[claim_dict])
    except Exception as e:
        # failed the response but passed the test
        assert True
        return

    assert False


# test valid insertion and retrieval
def test_valid_insertion(mock_db_session):
    pass
