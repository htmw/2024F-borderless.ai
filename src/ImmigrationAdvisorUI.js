import React, { useState } from 'react';
import './ImmigrationAdvisorUI.css';

const ImmigrationAdvisorUI = () => {
    const [startDate, setStartDate] = useState('');
    const [schoolName, setSchoolName] = useState('');
    const [mode, setMode] = useState('view');
    const [apiCallCount, setApiCallCount] = useState(0);
    const [pdfFile, setPdfFile] = useState(null);
    
    const handleApiCall = () => {
        console.log('API call with:', { startDate, schoolName });
        setApiCallCount(prev => prev + 1);
    };
    
    const toggleMode = () => {
        setMode(mode === 'view' ? 'edit' : 'view');
    };
    
    const handleFileChange = (event) => {
        setPdfFile(event.target.files[0]);
    };
    
    const handleFileUpload = () => {
        if (pdfFile) {
        console.log('Uploading file:', pdfFile.name);
        // Here you would typically send the file to your backend
        handleApiCall(); // Increment API call count when uploading
        }
    };
    
    return (
        <div className="container">
        <div className="logo">
            <img src="/borderless-ai-logo.png" alt="Borderless.AI Logo" />
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
            <button onClick={handleFileUpload} className="upload-btn">
            Upload PDF
            </button>
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
        </div>
    );
    };
    
    export default ImmigrationAdvisorUI;