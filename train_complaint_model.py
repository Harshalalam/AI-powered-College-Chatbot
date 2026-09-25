import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from preprocessing import preprocess_text


#Load the complaint dataset

df = pd.read_csv("data/complaints.csv")

print("Total complaints:", len(df))
print("\nCategory distribution:")
print(df["category"].value_counts())
print()


#Preprocess the text

df["cleaned"] = df["complaint"].apply(preprocess_text)


#Convert text to numbers (TF-IDF)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["cleaned"])
y = df["category"]

#Split into Train and Test

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)


#Train Model

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

#Evaluate the Model

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))


#Save Model and Vectorizer

with open("models/complaint_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("models/tfidf_complaint.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("\nComplaint model and vectorizer saved successfully!")
