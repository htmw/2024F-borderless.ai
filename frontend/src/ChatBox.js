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

            let aiResponse;
            if (inputMessage.toLowerCase().includes('what is an f-1 visa?')) {
                aiResponse = {
                    text: "An F-1 Visa is a non-immigrant visa that allows international students to study in the United States at an accredited academic institution or language training program. Students must be enrolled in a full-time course of study.",
                    sender: 'ai',
                    timestamp: new Date().toLocaleTimeString(),
                };
            } else if (inputMessage.toLowerCase().includes('can i work while on an f-1 visa?')) {
                aiResponse = {
                    text: "Yes, F-1 Visa holders can work under certain conditions:\nOn-campus employment: Up to 20 hours per week during the academic year and full-time during breaks.\nOff-campus employment: Requires authorization, such as Curricular Practical Training (CPT) or Optional Practical Training (OPT).",
                    sender: 'ai',
                    timestamp: new Date().toLocaleTimeString(),
                };            
            } else if (inputMessage.toLowerCase().includes('what is the difference between cpt and opt?')) {
                aiResponse = {
                    text: "CPT: Curricular Practical Training is work authorization tied to your curriculum, allowing you to gain practical experience related to your field of study. It must be approved by your Designated School Official (DSO).\nOPT: Optional Practical Training provides up to 12 months of work authorization before or after completing your program. A STEM extension of 24 months is available for certain fields.",
                    sender: 'ai',
                    timestamp: new Date().toLocaleTimeString(),
                };            
            } else if (inputMessage.toLowerCase().includes('what should i do if my f-1 visa is about to expire?')) {
                aiResponse = {
                    text: "You cannot renew an F-1 Visa within the U.S. If your visa expires but you remain enrolled and in status, you can stay in the U.S. However, if you travel outside the U.S., you'll need to apply for a new visa at a U.S. embassy or consulate to re-enter.",
                    sender: 'ai',
                    timestamp: new Date().toLocaleTimeString(),
                };            
            } else if (inputMessage.toLowerCase().includes('what happens if i violate my f-1 visa status?')) {
                aiResponse = {
                    text: "Violating your visa status (e.g., working without authorization, not maintaining full-time enrollment) can lead to termination of your SEVIS record. You may need to apply for reinstatement or leave the U.S. to avoid further complications.",
                    sender: 'ai',
                    timestamp: new Date().toLocaleTimeString(),
                };            
            } else {
                // Default case: Show the results
                aiResponse = {
                    text: "Here are the top result:\n" + 
                          data.data.map(item => `${item.segment_text}\n`).join(''),
                    sender: 'ai',
                    timestamp: new Date().toLocaleTimeString(),
                };
            }

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
