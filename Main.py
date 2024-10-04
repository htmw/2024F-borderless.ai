from flask import Flask, request, jsonify
import pdfplumber

app = Flask(__name__)

def extract_key_value_pairs(pdf_path):
    data = {}
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text().split("\n")
            for i, line in enumerate(text):
                if "SURNAME/PRIMARY NAME" in line:
                    if i + 1 < len(text):
                        data['SURNAME/PRIMARY NAME'] = text[i + 1].strip()
                elif "DATE OF BIRTH" in line:
                    if i + 1 < len(text):
                        data['DATE OF BIRTH'] = text[i + 1].strip()
                # Add other fields as needed
    return data

@app.route('/')
def index():
    return 'Hello from Flask!'

@app.route('/extract', methods=['POST'])
def extract():
    if 'pdf' not in request.files:
        return jsonify({"error": "No PDF file found in the request."}), 400

    pdf = request.files['pdf']

    # Save the uploaded PDF file temporarily
    pdf_path = '/tmp/uploaded_pdf.pdf'
    pdf.save(pdf_path)

    # Extract the data from the PDF
    extracted_data = extract_key_value_pairs(pdf_path)

    # Return the extracted data as a JSON response
    return jsonify(extracted_data)

if __name__ == '__main__':
    app.run(debug=True)
