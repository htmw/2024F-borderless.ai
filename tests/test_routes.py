import pytest
from fastapi.testclient import TestClient
from Main import app  # Ensure this matches the filename exactly

@pytest.fixture
def client():
    return TestClient(app)

def upload_pdf(client):
    """Helper function to upload the PDF and return the response."""
    with open("tests/I-20_ThippeganahalliCharudatta_Santhosh_N0033630590_travel signature.pdf", "rb") as pdf_file:
        response = client.post("/upload-pdf/", files={"file": ("sample.pdf", pdf_file, "application/pdf")})
    return response

def test_request_success(client):
    response = upload_pdf(client)
    assert response.status_code == 200

def test_resource_found(client):
    response = upload_pdf(client)
    response_data = response.json()  # Get the JSON response data
    assert "data" in response_data  # Check that 'data' exists in the response

def test_pdf_processed(client):
    response = upload_pdf(client)
    response_data = response.json()  # Get the JSON response data

    # Check for specific fields and values
    assert response_data["data"]["SURNAME/PRIMARY NAME"] == "Thippeganahalli", \
        f"Expected 'Thippeganahalli', but got {response_data['data']['SURNAME/PRIMARY NAME']}"

    assert response_data["data"]["DATE OF BIRTH"] == "14 OCTOBER 1999", \
        f"Expected '14 OCTOBER 1999', but got {response_data['data']['DATE OF BIRTH']}"  # Replace with the actual expected value

    # Continue adding assertions for other fields as needed
