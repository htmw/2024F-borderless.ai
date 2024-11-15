import React, { useState, useRef, useEffect } from 'react';
import { Search, Moon, Sun, Paperclip, Smile, Send } from 'lucide-react';
import data from '@emoji-mart/data';
import Picker from '@emoji-mart/react';

const ChatBox = () => {
    const [inputMessage, setInputMessage] = useState('');
    const [messages, setMessages] = useState([
        {
            text: "Hello! I'm your Immigration AI Assistant. How can I help you today?",
            sender: 'ai',
            timestamp: new Date().toLocaleTimeString(),
            reactions: []
        }
    ]);
    const [isLoading, setIsLoading] = useState(false);
    const [darkMode, setDarkMode] = useState(false);
    const [showEmojiPicker, setShowEmojiPicker] = useState(false);
    const [searchQuery, setSearchQuery] = useState('');
    const [showSearch, setShowSearch] = useState(false);
    const [pdfPreview, setPdfPreview] = useState(null);
    const fileInputRef = useRef(null);
    const messagesEndRef = useRef(null);

    const handleSendMessage = async () => {
        if (!inputMessage.trim()) return;

        const newMessage = {
            text: inputMessage,
            sender: 'user',
            timestamp: new Date().toLocaleTimeString(),
            reactions: []
        };
        
        setMessages(prev => [...prev, newMessage]);
        setInputMessage('');
        setIsLoading(true);

        try {
            const response = await fetch('http://localhost:8000/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: inputMessage }),
            });
            
            const data = await response.json();
            
            const aiResponse = {
                text: data.response || "I'm here to help with your immigration-related questions.",
                sender: 'ai',
                timestamp: new Date().toLocaleTimeString(),
                reactions: []
            };
            
            setMessages(prev => [...prev, aiResponse]);
        } catch (error) {
            const errorMessage = {
                text: "Sorry, I'm having trouble connecting right now. Please try again later.",
                sender: 'ai',
                timestamp: new Date().toLocaleTimeString(),
                reactions: []
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleFileUpload = async (file) => {
        if (!file) return;

        const uploadMessage = {
            text: `Uploading file: ${file.name}`,
            sender: 'user',
            timestamp: new Date().toLocaleTimeString(),
            reactions: []
        };
        setMessages(prev => [...prev, uploadMessage]);
        setIsLoading(true);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('http://localhost:8000/upload-pdf/', {
                method: 'POST',
                body: formData,
            });
            
            const data = await response.json();
            
            const responseMessage = {
                text: data.text || "Successfully processed your document.",
                sender: 'ai',
                timestamp: new Date().toLocaleTimeString(),
                reactions: []
            };
            setMessages(prev => [...prev, responseMessage]);

            // Create PDF preview if possible
            const fileReader = new FileReader();
            fileReader.onload = () => setPdfPreview(fileReader.result);
            fileReader.readAsDataURL(file);

        } catch (error) {
            const errorMessage = {
                text: "Sorry, there was an error processing your file.",
                sender: 'ai',
                timestamp: new Date().toLocaleTimeString(),
                reactions: []
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const addReaction = (messageIndex, emoji) => {
        setMessages(messages.map((msg, idx) => 
            idx === messageIndex
                ? { ...msg, reactions: [...new Set([...msg.reactions, emoji])] }
                : msg
        ));
    };

    const filteredMessages = searchQuery
        ? messages.filter(msg => 
            msg.text.toLowerCase().includes(searchQuery.toLowerCase()))
        : messages;

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    return (
        <div className={`chat-container ${darkMode ? 'dark' : ''}`}>
            {/* Chat Header */}
            <div className="chat-header">
                <h3>Immigration AI Assistant</h3>
                <div className="header-actions">
                    <button onClick={() => setShowSearch(!showSearch)}>
                        <Search size={20} />
                    </button>
                    <button onClick={() => setDarkMode(!darkMode)}>
                        {darkMode ? <Sun size={20} /> : <Moon size={20} />}
                    </button>
                </div>
            </div>

            {/* Search Bar */}
            {showSearch && (
                <div className="search-bar">
                    <input
                        type="text"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        placeholder="Search messages..."
                    />
                </div>
            )}

            {/* Messages */}
            <div className="messages-container">
                {filteredMessages.map((message, index) => (
                    <div
                        key={index}
                        className={`message ${message.sender}`}
                        onDoubleClick={() => setShowEmojiPicker(index)}
                    >
                        <div className="message-content">
                            {message.text}
                        </div>
                        {message.reactions.length > 0 && (
                            <div className="reactions">
                                {message.reactions.map((reaction, i) => (
                                    <span key={i}>{reaction}</span>
                                ))}
                            </div>
                        )}
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

            {/* PDF Preview */}
            {pdfPreview && (
                <div className="pdf-preview">
                    <embed src={pdfPreview} type="application/pdf" width="100%" height="200px" />
                    <button onClick={() => setPdfPreview(null)}>Close Preview</button>
                </div>
            )}

            {/* Emoji Picker */}
            {showEmojiPicker && (
                <div className="emoji-picker">
                    <Picker
                        data={data}
                        onEmojiSelect={(emoji) => {
                            addReaction(showEmojiPicker, emoji.native);
                            setShowEmojiPicker(false);
                        }}
                    />
                </div>
            )}

            {/* Input Area */}
            <div className="input-area">
                <input
                    type="file"
                    accept=".pdf"
                    ref={fileInputRef}
                    style={{ display: 'none' }}
                    onChange={(e) => handleFileUpload(e.target.files[0])}
                />
                <button
                    className="attachment-btn"
                    onClick={() => fileInputRef.current.click()}
                >
                    <Paperclip size={20} />
                </button>
                <button
                    className="emoji-btn"
                    onClick={() => setShowEmojiPicker(!showEmojiPicker)}
                >
                    <Smile size={20} />
                </button>
                <input
                    type="text"
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    placeholder="Type your message..."
                    onKeyPress={(e) => {
                        if (e.key === 'Enter') handleSendMessage();
                    }}
                />
                <button
                    className="send-btn"
                    onClick={handleSendMessage}
                    disabled={!inputMessage.trim()}
                >
                    <Send size={20} />
                </button>

            </div>
        </div>
    );
};

export default ChatBox;