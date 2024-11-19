import React, { useState, useRef, useEffect } from 'react';
import { Paperclip, Send } from 'lucide-react';

const ChatBox = ({ darkMode }) => {
    const [inputMessage, setInputMessage] = useState('');
    const [messages, setMessages] = useState([
        {
            text: "Hello! I'm your Immigration AI Assistant. How can I help you today?",
            sender: 'ai',
            timestamp: new Date().toLocaleTimeString(),
        },
    ]);
    const [isLoading, setIsLoading] = useState(false);
    const fileInputRef = useRef(null);
    const messagesEndRef = useRef(null);

    const handleSendMessage = async () => {
        if (!inputMessage.trim()) return;

        const newMessage = {
            text: inputMessage,
            sender: 'user',
            timestamp: new Date().toLocaleTimeString(),
        };

        setMessages((prev) => [...prev, newMessage]);
        setInputMessage('');
        setIsLoading(true);

        try {
            const response = await fetch('http://localhost:8000/query/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: inputMessage }),
            });
            const data = await response.json();

            if (data.error) {
                throw new Error(data.error);
            }

            const aiResponse = {
                text: "Here are the top results:\n" + data.data.map(item => `${item.segment_text}\n`).join(''),
                sender: 'ai',
                timestamp: new Date().toLocaleTimeString(),
            };

            setMessages((prev) => [...prev, aiResponse]);
        } catch (error) {
            setMessages((prev) => [
                ...prev,
                {
                    text: "Sorry, I'm having trouble processing your request right now. Please try again later.",
                    sender: 'ai',
                    timestamp: new Date().toLocaleTimeString(),
                },
            ]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleFileUpload = async (file) => {
        if (!file) return;

        setMessages((prev) => [
            ...prev,
            {
                text: `Uploading file: ${file.name}`,
                sender: 'user',
                timestamp: new Date().toLocaleTimeString(),
            },
        ]);
        
        setIsLoading(true);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('http://localhost:8000/upload-pdf/', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            if (response.ok) {
                const extractedMessage = {
                    text: `Extracted Information:\n- Surname: ${
                        data.data["SURNAME/PRIMARY NAME"] || "N/A"
                    }\n- Date of Birth: ${
                        data.data["DATE OF BIRTH"] || "N/A"
                    }`,
                    sender: 'ai',
                    timestamp: new Date().toLocaleTimeString(),
                };
                setMessages((prev) => [...prev, extractedMessage]);
            } else {
                setMessages((prev) => [
                    ...prev,
                    {
                        text: data.error || "Error processing the document.",
                        sender: 'ai',
                        timestamp: new Date().toLocaleTimeString(),
                    },
                ]);
            }
        } catch (error) {
            setMessages((prev) => [
                ...prev,
                {
                    text: "Failed to upload or process the file.",
                    sender: 'ai',
                    timestamp: new Date().toLocaleTimeString(),
                },
            ]);
        } finally {
            setIsLoading(false);
        }
    };

    const formatResponse = (data) => {
        return data
            .map(
                (item) =>
                    `Document ID: ${item.document_id}\nSegment Index: ${item.segment_index}\nSegment Text: ${item.segment_text}\nSimilarity Score: ${item.similarity_score}`
            )
            .join('\n\n');
    };

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    return (
        <div className={`chat-container ${darkMode ? 'dark' : ''}`}>
            {/* Chat Header */}
            <div className="chat-header">
                <h3>Immigration AI Assistant</h3>
            </div>

            {/* Messages */}
            <div className="messages-container">
                {messages.map((message, index) => (
                    <div key={index} className={`message-${message.sender}`}>
                        <div className="message-content">{message.text}</div>
                        <div className="message-timestamp">{message.timestamp}</div>
                    </div>
                ))}
                {isLoading && (
                    <div className="loading-indicator">
                        <div className="typing-dots">
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="input-area">
                <input
                    type="file"
                    accept=".pdf"
                    ref={fileInputRef}
                    style={{ display: 'none' }}
                    onChange={(e) => handleFileUpload(e.target.files[0])}
                />
                <button onClick={() => fileInputRef.current.click()} className="attachment-btn">
                    <Paperclip size={20} />
                </button>
                <input
                    type="text"
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    placeholder="Type your message..."
                    onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                />
                <button onClick={handleSendMessage} disabled={!inputMessage.trim()}>
                    <Send size={20} />
                </button>
            </div>
        </div>
    );
};

export default ChatBox;
