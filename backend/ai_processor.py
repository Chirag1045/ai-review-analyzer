from transformers import pipeline

# Initialize all our AI "chefs"
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
summarizer = pipeline("summarization", model="t5-small")
topic_spotter = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# --- MODEL UPGRADE ---
# We are hiring a more powerful "gourmet chef" for writing responses.
# This model is better at generating coherent and empathetic text.
response_generator = pipeline("text2text-generation", model="t5-base")

def analyze_sentiment(text):
    """Analyzes if text is POSITIVE or NEGATIVE."""
    try:
        result = sentiment_analyzer(text)
        return {"label": result[0]['label'], "score": round(result[0]['score'], 2)}
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return {"label": "UNKNOWN", "score": 0}

def summarize_text(text):
    """Creates a short summary of the text."""
    try:
        summary = summarizer(text, max_length=50, min_length=15, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print(f"Error in summarization: {e}")
        return "Could not generate summary."

def extract_topics(text):
    """Finds the most relevant topics from a predefined list."""
    try:
        candidate_labels = ["Service", "Price", "Quality", "Location", "Ambiance", "Speed", "Staff"]
        results = topic_spotter(text, candidate_labels)
        return results['labels'][:3]
    except Exception as e:
        print(f"Error in topic extraction: {e}")
        return []

def generate_response(review_text):
    """Generates a professional customer service response for a negative review."""
    try:
        # A detailed prompt to guide the AI model effectively.
        prompt = f"Write a professional and empathetic customer service response to the following negative review. Start with an apology, address the main issue mentioned in the review, and offer a way to make things right. Do not ask for contact information. Review: '{review_text}'"
        
        # Generate the response using our new, upgraded specialist.
        response = response_generator(prompt, max_length=100, num_beams=4, early_stopping=True)
        return response[0]['generated_text']
    except Exception as e:
        print(f"Error generating response: {e}")
        # Provide a fallback response in case of an error.
        return "We sincerely apologize for the issues you experienced. We are looking into this matter to ensure it doesn't happen again."

