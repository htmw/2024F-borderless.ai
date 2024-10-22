import React, { useState } from 'react';

const PdfUploader = () => {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://127.0.0.1:8000/upload-pdf/', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setResult(data.text || data.error);
    } catch (error) {
      console.error('Error uploading file:', error);
      setResult('Failed to upload file');
    }
  };

  return (
    <div>
      <input type="file" accept=".pdf" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload PDF</button>
      <div>
        <h3>Result:</h3>
        <pre>{result}</pre>
      </div>
    </div>
  );
};

export default PdfUploader;
