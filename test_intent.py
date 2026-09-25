import pickle
from preprocessing import preprocess_text

# Load model and vectorizer
with open("models/intent_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("models/tfidf_intent.pkl", "rb") as f:
    vectorizer = pickle.load(f)

tests = [
    "hi",
    "hello good morning",
    "what is the fee structure",
    "wifi is not working",
    "thank you",
    "who is the prime minister",
    "when does the semester start",
    "I have a complaint"
]

print("----- Intent Prediction -----\n")

for text in tests:
    cleaned = preprocess_text(text)
    vector = vectorizer.transform([cleaned])
    prediction = model.predict(vector)[0]
    print(f"Text       : {text}")
    print(f"Predicted  : {prediction}")
    print("-" * 40)
