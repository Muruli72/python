import os
import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Ensure target directory exists
os.makedirs("models", exist_ok=True)

DATASET_URL = "https://raw.githubusercontent.com/justmarkham/DAT8/master/data/sms.tsv"

print("Downloading dataset...")
df = pd.read_csv(
    DATASET_URL,
    sep="\t",
    header=None,
    names=["label", "message"]
)

print(f"Dataset loaded: {len(df)} records")
print("\nClass distribution:")
print(df["label"].value_counts())

# Clean and encode labels
df.dropna(subset=["label", "message"], inplace=True)
df["message"] = df["message"].astype(str)
df["label"] = df["label"].map({"ham": 0, "spam": 1})

X = df["message"]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Extract TF-IDF features
vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    max_features=5000,
    ngram_range=(1, 2),
    sublinear_tf=True
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

print(f"\nTraining samples: {X_train_tfidf.shape[0]}")
print(f"Testing samples: {X_test_tfidf.shape[0]}")
print(f"Features: {X_train_tfidf.shape[1]}")

# Train Logistic Regression classifier
model = LogisticRegression(C=1.5, solver="liblinear", random_state=42)
print("\nTraining model...")
model.fit(X_train_tfidf, y_train)

# Evaluate model
y_pred = model.predict(X_test_tfidf)
accuracy = accuracy_score(y_test, y_pred)

print("\n" + "=" * 50)
print(f"Accuracy: {accuracy * 100:.2f}%")
print("=" * 50)
print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=["Ham", "Spam"]))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Save serialized model and vectorizer artifacts
joblib.dump(vectorizer, "models/tfidf_vectorizer.pkl")
joblib.dump(model, "models/scam_model.pkl")

print("\nModel saved successfully in 'models/' directory!")