import flask
from flask import request, jsonify
from flask_cors import CORS
import sqlite3
import os

# --- SIMPLIFIED ---
# We no longer need the token logic here. 
# ai_processor.py is now fully responsible for it.

# Import all our AI functions from the updated recipe book
from ai_processor import analyze_sentiment, summarize_text, extract_topics, generate_response

app = flask.Flask(__name__)
CORS(app)

# --- Database Setup ---
DB_NAME = "reviews.db"

def init_db():
    """Initializes the database and creates the 'reviews' table if it doesn't exist."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sentiment TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")

# --- API Endpoints (No changes needed in the routes) ---

@app.route('/analyze', methods=['POST'])
def analyze_reviews():
    """Analyzes reviews and generates responses for negative ones."""
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({"error": "No text provided"}), 400

    reviews = [review.strip() for review in text.split('\n') if review.strip()]
    results = []
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        for review in reviews:
            sentiment = analyze_sentiment(review)
            summary = summarize_text(review)
            topics = extract_topics(review)
            
            suggested_response = None
            if sentiment and sentiment.get('label') == 'NEGATIVE':
                suggested_response = generate_response(review)
            
            if sentiment and 'label' in sentiment:
                cursor.execute("INSERT INTO reviews (sentiment) VALUES (?)", (sentiment['label'],))

            results.append({
                "original_review": review,
                "sentiment": sentiment,
                "summary": summary,
                "topics": topics,
                "suggested_response": suggested_response 
            })
        
        conn.commit()
        conn.close()

    except Exception as e:
        print(f"An error occurred during analysis or DB operation: {e}")
        return jsonify({"error": "Failed to process reviews"}), 500

    return jsonify(results)

@app.route('/stats', methods=['GET'])
def get_stats():
    """Provides all-time statistics from the database."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM reviews WHERE sentiment = 'POSITIVE'")
        positive_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM reviews WHERE sentiment = 'NEGATIVE'")
        negative_count = cursor.fetchone()[0]

        total_count = positive_count + negative_count
        
        conn.close()
        
        return jsonify({
            "positive": positive_count,
            "negative": negative_count,
            "total": total_count
        })
    except Exception as e:
        print(f"Error fetching stats: {e}")
        return jsonify({"error": "Could not retrieve statistics"}), 500

# Call init_db when the application starts
init_db()

if __name__ == "__main__":
    app.run(debug=True, port=5000)

