import React, { useState, useRef, useEffect } from 'react';
import { askMathQuestion } from '../services/api';
import Message from './Message';

function ChatWindow() {
  const [input, setInput] = useState('');
  const [history, setHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const messageListRef = useRef(null);

  // Auto-scroll to bottom
  useEffect(() => {
    if (messageListRef.current) {
      messageListRef.current.scrollTop = messageListRef.current.scrollHeight;
    }
  }, [history]);

  const addMessageToHistory = (message) => {
    setHistory(prev => [...prev, message]);
  };

  const handleSendQuestion = async () => {
    if (!input.trim()) return;

    const userQuestion = input;
    setIsLoading(true);
    
    addMessageToHistory({
      question: userQuestion,
      solution: "...",
      source: "user",
      thread_id: `user-${Date.now()}`
    });
    setInput('');

    try {
      const agentResponse = await askMathQuestion(userQuestion);
      
      setHistory(prev => [
        ...prev.slice(0, -1), 
        agentResponse 
      ]);

    } catch (error) {
      console.error("Failed to ask question:", error);
      const errorDetail = error.response?.data?.detail || "An unknown error occurred.";
      
      setHistory(prev => [
        ...prev.slice(0, -1),
        {
          question: userQuestion,
          solution: `Error: ${errorDetail}`,
          source: "error",
          thread_id: `error-${Date.now()}`
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !isLoading) {
      handleSendQuestion();
    }
  };
  
  return (
    <div className="chat-window">
      {/* This is the new structure. The message-list is separate 
        from the input-area wrapper.
      */}
      
      {/* 1. THE MESSAGE LIST */}
      <div className="message-list" ref={messageListRef}>
        <div className="message-wrapper"> {/* Inner wrapper for centering */}
          
          {/* Welcome Message */}
          {history.length === 0 && (
            <div className="message-container agent">
              <div className="message-question">Hello!</div>
              <div className="message-solution">
                I am your Math Routing Agent. How can I help you today?
              </div>
            </div>
          )}
          
          {history.map((msg, index) => (
            <Message 
              key={msg.thread_id || index} 
              message={msg} 
              onRefinement={addMessageToHistory}
            />
          ))}
          {isLoading && (
            <div className="message-container agent">
              Thinking...
            </div>
          )}
        </div>
      </div>
      
      {/* 2. THE "FLOATING" INPUT AREA */}
      <div className="input-area-wrapper">
        <div className="input-area">
          <input 
            value={input} 
            onChange={e => setInput(e.target.value)} 
            onKeyPress={handleKeyPress}
            placeholder="Ask a math question..."
            disabled={isLoading}
          />
          <button onClick={handleSendQuestion} disabled={isLoading}>
            {/* Simple Send Arrow Icon */}
            &#10148;
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatWindow;

