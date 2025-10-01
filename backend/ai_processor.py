import requests
import os

# --- CORRECTED TOKEN LOADING LOGIC ---

def get_hf_token():
    """Finds the Hugging Face token in the environment or a local file."""
    token = os.environ.get("HF_TOKEN")
    if not token and os.path.exists(".hf_token"):
        try:
            with open(".hf_token", "r") as f:
                token = f.read().strip()
        except Exception as e:
            print(f"Error reading .hf_token file: {e}")
            return None
    return token

API_TOKEN = get_hf_token()

if API_TOKEN:
    print("✅ Hugging Face token loaded successfully.")
else:
    print("❌ WARNING: Hugging Face token not found. API calls will likely fail.")

HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

# --- UPGRADED API FUNCTION ---

def query_api(payload, model_url):
    """General function to make a request to the Hugging Face API."""
    if not API_TOKEN:
        print("Cannot query API without a token.")
        return None
    
    print(f"Querying API: {model_url}...")
    try:
        response = requests.post(model_url, headers=HEADERS, json=payload, timeout=90)
        response.raise_for_status() 
        print(f"✅ Success from {model_url}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ API request failed for {model_url}: {e}")
        if e.response is not None:
            print(f"API Response Content: {e.response.text}")
        return None

# --- UPGRADED FUNCTIONS ---

def analyze_sentiment(text):
    """Analyzes sentiment with a common-sense override for nuanced negatives."""
    # --- NEW: Common Sense Override Logic ---
    # This rule-based check catches cases the AI model might misinterpret.
    negative_context_words = ["too", "overly", "wasn't very", "not that"]
    text_lower = text.lower()
    
    # Check if a negative context word is present.
    for word in negative_context_words:
        if word in text_lower:
            # Check for positive words that are likely being negated.
            if any(p_word in text_lower for p_word in ["sweet", "good", "great", "nice", "strong"]):
                 print("📝 Common sense override: Negative context detected for a positive word.")
                 # Assign a confident negative score, bypassing the AI.
                 return {"label": "NEGATIVE", "score": 0.90}

    # If no override is triggered, proceed with the AI model analysis.
    API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
    data = query_api({"inputs": text}, API_URL)
    if data and data[0]:
        top_result = max(data[0], key=lambda x: x['score'])
        label = top_result['label'].upper()
        # Standardize labels from the model
        if label == 'LABEL_2': label = 'POSITIVE'
        elif label == 'LABEL_0': label = 'NEGATIVE'
        else: label = 'NEUTRAL'
        score = top_result['score']
        return {"label": label, "score": round(score, 2)}
        
    return {"label": "UNKNOWN", "score": 0}

def summarize_text(text):
    """Summarizes text, but only if it's long enough to need a summary."""
    if len(text.split()) <= 10:
        print("📝 Short review detected, skipping AI summarization.")
        return text

    API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
    payload = {
        "inputs": text,
        "parameters": {"min_length": 10, "max_length": 40}
    }
    data = query_api(payload, API_URL)
    if data and data[0] and 'summary_text' in data[0]:
        return data[0]['summary_text']
    return "Could not generate summary."

def extract_topics(text):
    """Extracts topics using a faster, more reliable model."""
    API_URL = "https://api-inference.huggingface.co/models/valhalla/distilbart-mnli-12-3"
    payload = {
        "inputs": text,
        "parameters": {"candidate_labels": ["Service", "Price", "Quality", "Location", "Ambiance", "Speed", "Staff"]}
    }
    data = query_api(payload, API_URL)
    if data and 'labels' in data:
        return data['labels'][:3]
    return []

def generate_response(review_text):
    """Generates a specific and empathetic response using an improved prompt."""
    # --- NEW: Upgraded, More Specific Prompt ---
    # This guides the AI to provide a much more relevant and helpful response.
    prompt = f"""
    Act as a helpful and empathetic customer service manager for a cafe.
    A customer left the following negative review: "{review_text}"

    Your task is to write a short, professional response (2-3 sentences).
    1. Start with a sincere apology (e.g., "We're so sorry to hear...").
    2. Specifically acknowledge the main problem from their review (e.g., "cold coffee," "slow service").
    3. Reassure them that this is not the standard they should expect and that you will address the issue with your team.
    
    Do not ask them to contact you.
    
    Response:
    """
    API_URL = "https://api-inference.huggingface.co/models/google-t5/t5-base"
    data = query_api({"inputs": prompt}, API_URL)
    if data and data[0] and 'generated_text' in data[0]:
        return data[0]['generated_text']
    # A more specific fallback response
    return "We sincerely apologize for your experience. This is not the standard we aim for, and we will be looking into this with our team."

