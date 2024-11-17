from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pdfplumber
import io
from sandbox import query_pinecone  # Import the function from sandbox.py
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model for query endpoint
class QueryRequest(BaseModel):
    query: str

# Function to extract key-value pairs from PDF
def extract_key_value_pairs(pdf_content):
    data = {}
    try:
        with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
            for page in pdf.pages:
                text = page.extract_text().split("\n")
                for i, line in enumerate(text):
                    if i + 1 < len(text):
                        fields = line.split()
                        values_line = text[i + 1].strip()
                        values = values_line.split()

                        if "SURNAME/PRIMARY NAME" in line:
                            data["SURNAME/PRIMARY NAME"] = values[0]
                        if "DATE OF BIRTH" in line:
                            data["DATE OF BIRTH"] = " ".join(values[-3:])
                        if "CITY OF BIRTH" in line:
                            data["CITY OF BIRTH"] = " ".join(values[:2])
    except Exception as e:
        logging.error(f"Error extracting PDF data: {str(e)}")
        raise Exception(f"Error extracting PDF data: {str(e)}")
    return data

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return JSONResponse(status_code=400, content={"error": "File must be a PDF."})
    try:
        pdf_content = await file.read()
        extracted_data = extract_key_value_pairs(pdf_content)
        return JSONResponse(content={"data": extracted_data})
    except Exception as e:
        logging.error(f"Error processing PDF: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/query/")
async def query(request: QueryRequest):
    logging.info(f"Received query: {request.query}")
    try:
        results = query_pinecone(request.query)
        logging.info("Query processed successfully.")
        return JSONResponse(content={"data": results})
    except Exception as e:
        logging.error(f"Error processing query: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
