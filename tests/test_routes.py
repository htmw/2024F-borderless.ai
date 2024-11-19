import pytest
from fastapi.testclient import TestClient
from Main import app

@pytest.fixture
def client():
    return TestClient(app)

def upload_pdf(client, filename="tests/I-20_ThippeganahalliCharudatta_Santhosh_N0033630590_travel signature.pdf"):
    """Helper function to upload a PDF and return the response."""
    with open(filename, "rb") as pdf_file:
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
        f"Expected '14 OCTOBER 1999', but got {response_data['data']['DATE OF BIRTH']}"

def test_invalid_file_type(client):
    """Test uploading a non-PDF file."""
    response = client.post("/upload-pdf/", files={"file": ("sample.txt", b"Not a PDF", "text/plain")})
    assert response.status_code == 400
    assert response.json() == {"error": "File must be a PDF."}

def test_pdf_with_no_text(client):
    """Test uploading a PDF with no extractable text."""
    empty_pdf_path = "tests/empty.pdf"  # Create an empty PDF for this test
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.output("tests/empty.pdf")
    response = upload_pdf(client, filename=empty_pdf_path)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["data"] == {}, "Expected no data for an empty PDF"

def test_query_success(client):
    """Test querying the /query/ endpoint with a valid query."""
    payload = {"query": "What are the requirements for an F-1 visa?"}
    response = client.post("/query/", json=payload)
    assert response.status_code == 200
    assert "data" in response.json()  # Check that 'data' exists in the response  

def test_query_empty_payload(client):
    """Test /query/ endpoint with an empty payload."""
    payload = {}
    response = client.post("/query/", json=payload)
    assert response.status_code == 422  # Unprocessable Entity (validation error)

def test_query_invalid_payload(client):
    """Test /query/ endpoint with invalid payload structure."""
    payload = {"invalid_field": "Test query"}
    response = client.post("/query/", json=payload)
    assert response.status_code == 422  # Unprocessable Entity (validation error)

def test_cors_headers(client):
    """Ensure CORS headers are set for the API."""
    response = client.options("/query/")
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "*"