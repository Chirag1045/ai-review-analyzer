import React, { useState, useEffect, useMemo } from "react";
import axios from "axios";

// --- SVG Icon Components ---
const SparkleIcon = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="20"
    height="20"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M12 2L14.5 9.5L22 12L14.5 14.5L12 22L9.5 14.5L2 12L9.5 9.5L12 2z" />
  </svg>
);
const ThumbsUpIcon = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="16"
    height="16"
    viewBox="0 0 24 24"
    fill="currentColor"
  >
    <path d="M1 21h4V9H1v12zm22-11c0-1.1-.9-2-2-2h-6.31l.95-4.57.03-.32c0-.41-.17-.79-.44-1.06L14.17 1 7.59 7.59C7.22 7.95 7 8.45 7 9v10c0 1.1.9 2 2 2h9c.83 0 1.54-.5 1.84-1.22l3.02-7.05c.09-.23.14-.47.14-.73v-2z" />
  </svg>
);
const ThumbsDownIcon = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="16"
    height="16"
    viewBox="0 0 24 24"
    fill="currentColor"
  >
    <path d="M15 3H6c-.83 0-1.54.5-1.84 1.22l-3.02 7.05c-.09.23-.14.47-.14.73v2c0 1.1.9 2 2 2h6.31l-.95 4.57-.03.32c0 .41-.17-.79-.44 1.06L9.83 23l6.59-6.59c.36-.36.58-.86.58-1.41V5c0-1.1-.9-2-2-2zm4 0v12h4V3h-4z" />
  </svg>
);
const HistoryIcon = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M1 4v6h6" />
    <path d="M3.51 15a9 9 0 1 0 2.19-9.51L1 10" />
  </svg>
);
const ResponseIcon = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="16"
    height="16"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z" />
  </svg>
);

// --- UI Components ---
const Loader = () => (
  <div className="loader-container">
    <div className="loader"></div>
    <p style={{ marginTop: "1rem", color: "var(--text-secondary)" }}>
      AI chefs are analyzing your reviews...
    </p>
  </div>
);
const ErrorMessage = ({ message }) => (
  <div className="error-container">
    <p className="error-message">{message}</p>
  </div>
);

const ResultCard = ({ result }) => {
  const isPositive = result.sentiment.label === "POSITIVE";

  return (
    <div className="result-card">
      <p
        style={{
          fontStyle: "italic",
          borderLeft: "3px solid var(--border-color)",
          paddingLeft: "1rem",
        }}
      >
        "{result.original_review}"
      </p>
      <hr
        style={{
          border: "none",
          height: "1px",
          backgroundColor: "var(--border-color)",
          margin: "1rem 0",
        }}
      />
      <p>
        <strong>Summary:</strong> {result.summary}
      </p>
      <p>
        <strong>Sentiment:</strong>
        <span
          className={`sentiment-badge ${isPositive ? "positive" : "negative"}`}
        >
          {isPositive ? <ThumbsUpIcon /> : <ThumbsDownIcon />}
          {result.sentiment.label} ({result.sentiment.score})
        </span>
      </p>
      <div>
        <strong>Key Topics:</strong>
        <div className="topics-container">
          {result.topics.map((topic) => (
            <span key={topic} className="topic-pill">
              {topic}
            </span>
          ))}
        </div>
      </div>
      {result.suggested_response && (
        <div className="suggested-response">
          <h4>
            <ResponseIcon /> AI-Powered Suggested Response
          </h4>
          <p>{result.suggested_response}</p>
        </div>
      )}
    </div>
  );
};

const OverallSentimentCard = ({ results }) => {
  const sentimentStats = useMemo(() => {
    const positiveCount = results.filter(
      (r) => r.sentiment.label === "POSITIVE"
    ).length;
    const totalCount = results.length;
    const percentage =
      totalCount > 0 ? Math.round((positiveCount / totalCount) * 100) : 0;
    return { positiveCount, totalCount, percentage };
  }, [results]);

  return (
    <div className="summary-card">
      <h3>Current Batch Sentiment</h3>
      <div className="sentiment-bar">
        <div
          className="sentiment-bar-fill"
          style={{ width: `${sentimentStats.percentage}%` }}
        ></div>
      </div>
      <p>
        <strong>{sentimentStats.percentage}% Positive</strong> (
        {sentimentStats.positiveCount} of {sentimentStats.totalCount} reviews)
      </p>
    </div>
  );
};

const HistoricalStatsCard = ({ stats }) => {
  const positivePercent =
    stats.total > 0 ? Math.round((stats.positive / stats.total) * 100) : 0;

  return (
    <div className="summary-card">
      <h3>
        <HistoryIcon /> All-Time Stats
      </h3>
      <p>
        <strong>Total Reviews Analyzed:</strong> {stats.total}
      </p>
      <p>
        <strong>Overall Positive Sentiment:</strong> {positivePercent}%
      </p>
    </div>
  );
};

// --- Define the API's base URL ---
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5000";

function App() {
  // --- State Management ---
  const [reviewsText, setReviewsText] = useState("");
  const [analysisResults, setAnalysisResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [allTimeStats, setAllTimeStats] = useState({
    positive: 0,
    negative: 0,
    total: 0,
  });

  const fetchAllTimeStats = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/stats`);
      setAllTimeStats(response.data);
    } catch (err) {
      console.error("Could not fetch historical stats:", err);
    }
  };

  useEffect(() => {
    fetchAllTimeStats();
  }, []);

  const handleAnalyzeClick = async () => {
    if (!reviewsText.trim()) {
      setError("Please paste some reviews before analyzing.");
      return;
    }

    setIsLoading(true);
    setError("");
    setAnalysisResults([]);

    try {
      const response = await axios.post(`${API_BASE_URL}/analyze`, {
        text: reviewsText,
      });
      setAnalysisResults(response.data);
      fetchAllTimeStats();
    } catch (err) {
      console.error("Error communicating with the kitchen:", err);
      setError("Could not connect to the AI server. Is the backend running?");
    } finally {
      setIsLoading(false);
    }
  };

  // --- Render Logic ---
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>AI-Powered Insight Engine</h1>
        <p>
          Transform raw customer feedback into actionable intelligence. Paste
          your reviews below to unlock sentiment, summaries, and key topics in
          seconds.
        </p>
      </header>

      <main>
        <div className="input-area">
          <textarea
            value={reviewsText}
            onChange={(e) => setReviewsText(e.target.value)}
            placeholder="e.g., The coffee was amazing!..."
          />
          <div className="button-container">
            <button
              onClick={handleAnalyzeClick}
              disabled={isLoading}
              className="analyze-button"
            >
              <SparkleIcon />
              {isLoading ? "Analyzing..." : "Generate Insights"}
            </button>
          </div>
        </div>

        <div className="results-container">
          {isLoading && <Loader />}
          {error && <ErrorMessage message={error} />}
          {analysisResults.length > 0 && (
            <section className="results-section">
              <div className="summary-grid">
                <OverallSentimentCard results={analysisResults} />
                <HistoricalStatsCard stats={allTimeStats} />
              </div>
              <h2>Detailed Analysis Report</h2>
              {analysisResults.map((result, index) => (
                <ResultCard key={index} result={result} />
              ))}
            </section>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
