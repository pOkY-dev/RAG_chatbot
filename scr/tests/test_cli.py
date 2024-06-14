import pytest
from query_handler import handle_complex_queries

@pytest.fixture
def sample_query():
    return "Find an SUV in Spain"

def test_cli_chatbot(sample_query):
    response = handle_complex_queries(sample_query)
    assert "Brand" in response
    assert "Model" in response
    assert "Location" in response