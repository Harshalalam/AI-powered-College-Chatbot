from database import save_complaint
import pickle
import random
import json
from datetime import datetime
from preprocessing import preprocess_text

# ==========================================
# Load Models
# ==========================================
with open("models/intent_model.pkl", "rb") as f:
    intent_model = pickle.load(f)

with open("models/tfidf_intent.pkl", "rb") as f:
    intent_vectorizer = pickle.load(f)

with open("models/complaint_model.pkl", "rb") as f:
    complaint_model = pickle.load(f)

with open("models/tfidf_complaint.pkl", "rb") as f:
    complaint_vectorizer = pickle.load(f)

# ==========================================
# Load Intents (for responses)
# ==========================================
with open("data/intents.json", "r", encoding="utf-8") as f:
    intents_data = json.load(f)

# Create a dictionary for quick response lookup
intent_responses = {}
for intent in intents_data["intents"]:
    intent_responses[intent["tag"]] = intent["responses"]

# ==========================================
# Helper Functions
# ==========================================
def get_intent(text):
    cleaned = preprocess_text(text)
    vector = intent_vectorizer.transform([cleaned])
    intent = intent_model.predict(vector)[0]
    confidence = intent_model.predict_proba(vector).max()
    return intent, confidence

def get_complaint_category(text):
    cleaned = preprocess_text(text)
    vector = complaint_vectorizer.transform([cleaned])
    category = complaint_model.predict(vector)[0]
    confidence = complaint_model.predict_proba(vector).max()
    return category, confidence

def generate_ticket_id():
    now = datetime.now()
    return f"CMP{now.strftime('%Y%m%d%H%M%S')}"

def get_priority(text):
    text = text.lower()
    high_keywords = ["urgent", "emergency", "not working", "no water", "no electricity", 
                     "leakage", "spark", "fire", "broken", "completely down"]
    
    for word in high_keywords:
        if word in text:
            return "High"
    return "Medium"

# ==========================================
# Main Dialog Function
# ==========================================
def get_response(user_message):
    intent, intent_conf = get_intent(user_message)
    
    # Low confidence → treat as other
    if intent_conf < 0.15:
        intent = "other"
    
    # ---------- GREETING ----------
    if intent == "greeting":
        return random.choice(intent_responses["greeting"])
    
    # ---------- GOODBYE ----------
    elif intent == "goodbye":
        return random.choice(intent_responses["goodbye"])
 
   # ---------- COMPLAINT ----------
    elif intent == "complaint":
        category, conf = get_complaint_category(user_message)
        ticket_id = generate_ticket_id()
        priority = get_priority(user_message)
        
        # Save to database
        save_complaint(ticket_id, user_message, category, priority)
        
        response = (
            f"Your complaint has been registered successfully.\n\n"
            f"**Ticket ID**   : {ticket_id}\n"
            f"**Category**    : {category}\n"
            f"**Priority**    : {priority}\n"
            f"**Status**      : Pending\n\n"
            f"Our team will look into it soon."
        )
        return response    

    # ---------- COMPLAINT STATUS ----------
    elif intent == "complaint_status":
        return "Please provide your Complaint Ticket ID so I can check the status."
    
    # ---------- ENQUIRY INTENTS ----------
    elif intent.startswith("enquiry_"):
        return random.choice(intent_responses.get(intent, 
               ["Please contact the administration office for this information."]))
    
    # ---------- OTHER / UNKNOWN ----------
    else:
        return "I'm sorry, I can only help with college-related enquiries and complaints."
