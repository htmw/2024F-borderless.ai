from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import io

origins = [
    "http://localhost:3000",  # React frontend
]

app = FastAPI()

# Add CORS middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

def extract_key_value_pairs(pdf_content):
    data = {}

    # Create a PDF file-like object from the content
    with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
        for page in pdf.pages:
            text = page.extract_text().split("\n")
            for i, line in enumerate(text):
                # Ensure there's a next line to read for values
                if i + 1 < len(text):
                    # Split the field names and values
                    fields = line.split()  # Split the line into words (field names)
                    values_line = text[i + 1].strip()  # Next line for values
                    values = values_line.split()  # Split values line into words

                    # Depending on the number of fields, you can adjust accordingly
                    if "SURNAME/PRIMARY NAME" in line:
                        data["SURNAME/PRIMARY NAME"] = values[0]  # Adjust if necessary
                    if "DATE OF BIRTH" in line:
                        # We want the last value in the line for DATE OF BIRTH
                        data["DATE OF BIRTH"] = values [-3] + " " + values[-2] + " " + values[-1] # Should capture the full date

                    if "CITY OF BIRTH" in line:
                        data["CITY OF BIRTH"] = values[0] + " " + values[1]  # Combine city and state if necessary

    return data


@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        # Read the uploaded PDF file
        pdf_content = await file.read()
        
        # Process the PDF and extract key-value pairs
        extracted_data = extract_key_value_pairs(pdf_content)

        return JSONResponse(content={"data": extracted_data})

    except Exception as e:
        print(f"Error processing PDF: {str(e)}")  # Print the error message
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
