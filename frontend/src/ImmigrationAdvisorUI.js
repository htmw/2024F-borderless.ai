import React, { useState, useEffect } from 'react';
import './ImmigrationAdvisorUI.css';
import logo from './BorderlessAi.jpeg';
import ChatBox from './ChatBox';
import { Moon, Sun } from 'lucide-react';

const ImmigrationAdvisorUI = () => {
    const [startDate, setStartDate] = useState('');
    const [schoolName, setSchoolName] = useState('');
    const [mode, setMode] = useState('view');
    const [apiCallCount, setApiCallCount] = useState(0);
    const [result, setResult] = useState({});
    const [darkMode, setDarkMode] = useState(false);

    // Initialize dark mode from localStorage
    useEffect(() => {
        const savedMode = localStorage.getItem('darkMode') === 'true';
        setDarkMode(savedMode);
        if (savedMode) {
            document.documentElement.classList.add('dark-mode');
        }
    }, []);

    // Toggle dark mode
    const toggleDarkMode = () => {
        const newMode = !darkMode;
        setDarkMode(newMode);
        localStorage.setItem('darkMode', newMode);
        document.documentElement.classList.toggle('dark-mode');
    };

    return (
        <div className={`app-wrapper ${darkMode ? 'dark-mode' : ''}`}>
            {/* Theme Toggle Button */}
            <button 
                className="theme-toggle-btn"
                onClick={toggleDarkMode}
                aria-label={darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
            >
                {darkMode ? (
                    <Sun className="toggle-icon" size={24} />
                ) : (
                    <Moon className="toggle-icon" size={24} />
                )}
            </button>

            <div className="container">
                <div className="logo">
                    <img src={logo} alt="Borderless.AI Logo" />
                </div>
                <h1 className="title">Immigration AI Advisor</h1>

                <div className="card project-details">
                    <h2>Project Details</h2>
                    <p><strong>Team:</strong> Borderless.AI</p>
                    <p><strong>Problem Statement:</strong> International students face complex immigration-related questions.</p>
                    <p><strong>Project Description:</strong> AI-based application to assist international students with immigration-related queries.</p>
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

                {/* Chat Component */}
                <div className="chat-section">
                    <ChatBox darkMode={darkMode} />
                </div>
            </div>
        </div>
    );
};

export default ImmigrationAdvisorUI;