import pickle
from preprocessing import preprocess_text

with open("models/intent_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("models/tfidf_intent.pkl", "rb") as f:
    vectorizer = pickle.load(f)

tests = [
    "hi",
    "hello",
    "what is the fee structure",
    "wifi is not working",
    "there is no water in the class",
    "i want to know about scholarship",
    "thank you"
]

print("----- Debugging Intent Predictions -----\n")

for text in tests:
    cleaned = preprocess_text(text)
    vector = vectorizer.transform([cleaned])
    
    prediction = model.predict(vector)[0]
    confidence = model.predict_proba(vector).max()
    
    print(f"Text       : {text}")
    print(f"Predicted  : {prediction}")
    print(f"Confidence : {confidence:.3f}")
    print("-" * 45)
