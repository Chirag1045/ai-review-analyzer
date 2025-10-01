🤖 AI-Powered Insight Engine
A full-stack web application that transforms raw customer feedback into actionable business intelligence using modern AI models. This tool provides sentiment analysis, topic extraction, concise summarization, and AI-generated customer service responses for any given text.

**[View the Live Demo](https://ai-review-analyzer.vercel.app/)**

A placeholder for a screenshot of your beautiful application in action.

✨ Key Features
This project was built to move beyond simple prototypes and create a deployable, end-to-end AI solution that solves a real business problem.

Multi-Faceted AI Analysis: Processes customer reviews to extract:

Sentiment Analysis: Classifies feedback as POSITIVE or NEGATIVE with a confidence score.

Topic Extraction: Identifies the 3 most relevant topics (e.g., Service, Price, Quality) from a predefined list using zero-shot classification.

AI Summarization: Condenses long reviews into a single, easy-to-read sentence.

Actionable Response Generation: For every negative review, the application uses a t5-base model to generate a professional and empathetic customer service response, helping businesses resolve issues quickly.

Historical Trend Tracking: All review sentiments are stored in a local SQLite database, providing an "All-Time Stats" dashboard to track overall customer satisfaction over time.

Dynamic Frontend: A clean, responsive, and user-friendly interface built with React that provides real-time feedback, loading states, and clear data visualizations.

🛠️ Tech Stack
This project combines a powerful Python backend for AI processing with a modern React frontend for the user interface.

Backend (The "Kitchen"):

Framework: Python, Flask

AI & Machine Learning:

transformers (from Hugging Face) for accessing pre-trained models.

LangChain principles for structuring AI tasks.

Models Used: distilbert-base-uncased (Sentiment), t5-base (Response Generation), facebook/bart-large-mnli (Topic Extraction).

Database: SQLite

Frontend (The "Dining Room"):

Library: React.js (with Vite)

Styling: Custom CSS with a modern, professional design system.

API Communication: Axios

🚀 Getting Started
To get a local copy up and running, follow these simple steps.

Prerequisites
Python 3.8+

Node.js (LTS version)

Git

Installation & Setup
Clone the repository:

git clone [https://github.com/Chirag1045/ai-review-analyzer.git](https://github.com/Chirag1045/ai-review-analyzer.git)
cd ai-review-analyzer

Setup the Backend:

cd backend
python -m venv venv

# On Windows

venv\Scripts\activate

# On Mac/Linux

# source venv/bin/activate

pip install -r requirements.txt
python app.py

The backend server will start on http://127.0.0.1:5000.

Setup the Frontend:
(Open a new, separate terminal for this)

cd frontend
npm install
npm run dev
