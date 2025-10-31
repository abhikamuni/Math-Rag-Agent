import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";
// The API is running on http://localhost:8000
const API = axios.create({ baseURL: API_URL });

/**
 * Sends a new question to the backend.
 * @param {string} question The user's math question.
 * @param {string} student_id A placeholder ID.
 * @returns {Promise<object>} The agent's first response.
 */
export const askMathQuestion = async (question, student_id = "student1") => {
  const response = await API.post("/ask/", { question, student_id });
  return response.data; // { solution, source, thread_id, question }
};

/**
 * Sends user feedback to the backend.
 * @param {object} payload The feedback object.
 * @returns {Promise<object>} A new refined answer, or a simple status.
 */
export const sendFeedback = async (payload) => {
  // Payload should be:
  // { question, original_solution, feedback_text, rating, thread_id }
  const response = await API.post("/feedback/", payload);
  return response.data;
};

