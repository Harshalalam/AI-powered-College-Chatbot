import json
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from preprocessing import preprocess_text

# ==========================================
# 1. Load intents.json
# ==========================================
with open("data/intents.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# ==========================================
# 2. Prepare training data
# ==========================================
patterns = []
tags = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        patterns.append(preprocess_text(pattern))
        tags.append(intent["tag"])

print("Total training samples:", len(patterns))
print("Total intents:", len(set(tags)))
print("Intents:", set(tags))
print()

# ==========================================
# 3. Convert text to numbers using TF-IDF
# ==========================================
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(patterns)
y = tags

# ==========================================
# 4. Split data (Train + Test)
# ==========================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ==========================================
# 5. Train the Model
# ==========================================
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# ==========================================
# 6. Evaluate the Model
# ==========================================
y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# ==========================================
# 7. Save the Model and Vectorizer
# ==========================================
with open("models/intent_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("models/tfidf_intent.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("\nModel and Vectorizer saved successfully in 'models/' folder")
