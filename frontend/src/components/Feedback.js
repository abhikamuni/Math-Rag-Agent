import React, { useState } from 'react';
import { sendFeedback } from '../services/api';

/**
 * The Feedback component.
 * @param {object} props
 * @param {object} props.message The full message object { question, solution, thread_id }
 * @param {function} props.onRefinement A function to add a new message to the chat history
 */
function Feedback({ message, onRefinement }) {
  const [rating, setRating] = useState(null); // 'good' or 'bad'
  const [feedbackText, setFeedbackText] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async () => {
    if (!rating) {
      alert("Please select 'Good' or 'Bad' before submitting.");
      return;
    }

    setIsLoading(true);
    
    // 1. Create the feedback payload
    const payload = {
      question: message.question,
      original_solution: message.solution,
      feedback_text: feedbackText,
      rating: rating,
      thread_id: message.thread_id
    };

    try {
      // 2. Send feedback to the backend
      const response = await sendFeedback(payload);
      
      // 3. Hide this feedback box
      setIsSubmitted(true); 

      // 4. If the API sent back a new *refined* answer,
      //    add it to the main chat window.
      if (response && response.source === 'refined') {
        onRefinement(response);
      }

    } catch (error) {
      console.error("Failed to send feedback:", error);
      alert(`Failed to send feedback: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  if (isSubmitted) {
    return (
      <div className="feedback-box" style={{textAlign: 'center', fontStyle: 'italic', background: '#f8f9fa', border: 'none'}}>
        Thank you for your feedback!
      </div>
    );
  }

  return (
    <div className="feedback-box">
      <h4>Was this solution helpful?</h4>
      <div className="feedback-buttons">
        <button 
          onClick={() => setRating('good')}
          className={rating === 'good' ? 'selected-good' : ''}
          disabled={isLoading}
        >
          👍 Good
        </button>
        <button 
          onClick={() => setRating('bad')}
          className={rating === 'bad' ? 'selected-bad' : ''}
          disabled={isLoading}
        >
          👎 Bad
        </button>
      </div>

      {rating && (
        <div className="feedback-form">
          <textarea
            value={feedbackText}
            onChange={(e) => setFeedbackText(e.target.value)}
            placeholder={rating === 'bad' ? "How can we improve it?" : "What did you like?"}
            disabled={isLoading}
          />
          <button onClick={handleSubmit} disabled={isLoading}>
            {isLoading ? 'Submitting...' : 'Submit Feedback'}
          </button>
        </div>
      )}
    </div>
  );
}

export default Feedback;

