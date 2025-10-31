import React from 'react';
import Feedback from './Feedback';

/**
 * A simple function to render text with newlines and bolding.
 * This makes the agent's step-by-step solutions look much better.
 */
const renderSolution = (text) => {
  if (!text) return null;

  return text.split('\n').map((line, index) => {
    // Check for markdown-style bolding **text**
    const parts = line.split('**');
    return (
      <span key={index}>
        {parts.map((part, i) =>
          i % 2 === 1 ? <strong key={i}>{part}</strong> : part
        )}
        <br />
      </span>
    );
  });
};


function Message({ message, onRefinement }) {

  if (message.source === 'user') {
    return (
      <div className="message-container user">
        <div className="message-question">{message.question}</div>
      </div>
    );
  }

  // Determine the CSS class
  let containerClass = 'agent';
  if (message.source === 'error') containerClass = 'error';
  else if (message.source === 'refined') containerClass = 'refined';

  const showFeedback = (
    message.source === 'knowledge_base' || 
    message.source === 'web_search' ||
    message.source === 'direct_answer'
  );

  return (
    <div className={`message-container ${containerClass}`}>
      {/* Only show the question if it's an error or refined, 
          since the user's question is already visible */}
      {(message.source === 'error' || message.source === 'refined') && (
         <div className="message-question">{message.question}</div>
      )}
     
      <div className="message-solution">
        {renderSolution(message.solution)}
      </div>

      <div className="message-source">
        Source: {message.source}
      </div>
      
      {showFeedback && (
        <Feedback 
          message={message} 
          onRefinement={onRefinement} 
        />
      )}
    </div>
  );
}

export default Message;

