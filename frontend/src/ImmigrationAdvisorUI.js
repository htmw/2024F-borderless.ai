import React, { useState } from 'react';
import './ImmigrationAdvisorUI.css';
import logo from './BorderlessAi.jpeg';

const ImmigrationAdvisorUI = () => {
    const [startDate, setStartDate] = useState('');
    const [schoolName, setSchoolName] = useState('');
    const [mode, setMode] = useState('view');
    const [apiCallCount, setApiCallCount] = useState(0);
    const [pdfFile, setPdfFile] = useState(null);
    const [result, setResult] = useState({});
    
    const handleApiCall = async () => {
        console.log('API call with:', { startDate, schoolName });
        setApiCallCount(prev => prev + 1);
        
        if (!pdfFile) return;
    
        const formData = new FormData();
        formData.append('file', pdfFile);
    
        try {
            const response = await fetch('http://localhost:8000/upload-pdf/', {
                method: 'POST',
                body: formData,
                headers: {
                    'Accept': 'application/json',
                },
            });
            const data = await response.json();
            
            if (response.ok) {
                // Store the extracted fields (like SURNAME/PRIMARY NAME, DATE OF BIRTH) in result
                setResult(data.data); // Access the data returned from the backend
            } else {
                setResult({ error: data.error });
            }
        } catch (error) {
            console.error('Error uploading file:', error);
            setResult({ error: 'Failed to upload file' });
        }
    };
    
    const toggleMode = () => {
        setMode(mode === 'view' ? 'edit' : 'view');
    };
    
    const handleFileChange = (event) => {
        let pdfFile = event.target.files[0];
        setPdfFile(pdfFile);
    };
    
    const handleFileUpload = () => {
        if (pdfFile) {
            console.log('Uploading file:', pdfFile.name);
            handleApiCall(); // Increment API call count when uploading
        }
    };
    
    return (
        <div className="container">
            <div className="logo">
                <img src={logo} alt="Borderless.AI Logo" />
            </div>
            <h1 className="title">Immigration AI Advisor</h1>
    
            <div className="card project-details">
                <h2>Project Details</h2>
                <p><strong>Team:</strong> Borderless.AI</p>
                <p><strong>Problem Statement:</strong> International students face complex immigration-related questions, and existing processes for getting accurate advice are slow.</p>
                <p><strong>Project Description:</strong> AI-based application to assist international students with immigration-related queries by reading documents (I-20, I-94) and providing personalized advice.</p>
            </div>
    
            <div className="input-group">
                <div className="input-field">
                    <label htmlFor="startDate">Start date:</label>
                    <input
                        id="startDate"
                        type="date"
                        value={startDate}
                        onChange={(e) => setStartDate(e.target.value)}
                    />
                </div>
                <div className="input-field">
                    <label htmlFor="schoolName">School name:</label>
                    <input
                        id="schoolName"
                        type="text"
                        value={schoolName}
                        onChange={(e) => setSchoolName(e.target.value)}
                    />
                </div>
            </div>
    
            <div className="file-upload">
                <label htmlFor="pdfUpload">Upload PDF (I-20 or I-94):</label>
                <input
                    id="pdfUpload"
                    type="file"
                    accept=".pdf"
                    onChange={handleFileChange}
                />
            </div>
    
            <div className="action-buttons">
                <button onClick={handleFileUpload} className="api-btn">
                    <span className="plus">+</span>
                </button>
                <button onClick={toggleMode} className={`mode-btn ${mode === 'edit' ? 'active' : ''}`}>
                    {mode === 'view' ? '▶' : '◼'}
                </button>
                <span className="api-count">{apiCallCount}</span>
            </div>
    
            <div className="info">
                <p>1) Current Mode: {mode}</p>
                <p>2) API calls: {apiCallCount}</p>
                <p>3) Uploaded File: {pdfFile ? pdfFile.name : 'No file uploaded'}</p>
            </div>
    
            {result && (
                <div className="result">
                    <h3>Extracted Information</h3>
                    <p><strong>Surname/Primary Name:</strong> {result["SURNAME/PRIMARY NAME"] || "N/A"}</p>
                    <p><strong>Date of Birth:</strong> {result["DATE OF BIRTH"] || "N/A"}</p>
                    {/* Add more fields as necessary */}
                    {result.error && <p className="error">Error: {result.error}</p>}
                </div>
            )}
        </div>
    );
};

export default ImmigrationAdvisorUI;
