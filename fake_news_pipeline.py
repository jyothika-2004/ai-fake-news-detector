import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def main():
    print("--- Week 1: Data Loading & Cleaning ---")
    try:
        data = pd.read_csv("train.csv")
    except FileNotFoundError:
        print("Error: train.csv not found. Please provide the dataset or run create_dummy_data.py")
        return

    # Check if expected columns exist
    if 'text' not in data.columns or 'label' not in data.columns:
        # If columns are different, try to map them (common in various datasets)
        if 'title' in data.columns and 'text' in data.columns:
            data['text'] = data['title'] + " " + data['text']
        else:
            print("Error: Dataset must contain 'text' and 'label' columns.")
            return

    X = data['text']
    y = data['label']

    # Text cleaning function
    def clean_text(text):
        if not isinstance(text, str):
            text = str(text)
        text = re.sub(r'\W', ' ', text)  # remove punctuation
        text = text.lower() # lowercase
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    print("Cleaning text data...")
    X = X.apply(clean_text)

    print("\n--- Week 2: Feature Engineering ---")
    print("Applying TF-IDF Vectorization...")
    # Using max_features=5000 to limit dimensionality and speed up training
    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english') 
    X_vec = vectorizer.fit_transform(X)

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)
    print(f"Training set size: {X_train.shape[0]}, Test set size: {X_test.shape[0]}")

    print("\n--- Week 3 & 4: Model Building and Evaluation ---")
    models = {
        "KNN": KNeighborsClassifier(n_neighbors=5),
        "LogReg": LogisticRegression(max_iter=1000),
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
        "NeuralNet": MLPClassifier(hidden_layer_sizes=(100,), max_iter=300, random_state=42)
    }

    results = {}

    for name, model in models.items():
        print(f"\nTraining {name}...")
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        
        acc = accuracy_score(y_test, preds)
        results[name] = acc
        print(f"{name} Accuracy: {acc:.4f}")
        print("Classification Report:")
        print(classification_report(y_test, preds))
        
        # Plot confusion matrix
        cm = confusion_matrix(y_test, preds)
        plt.figure(figsize=(5,4))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Real', 'Fake'], yticklabels=['Real', 'Fake'])
        plt.title(f'{name} Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.savefig(f'{name}_confusion_matrix.png')
        plt.close()

    print("\n--- Summary ---")
    for name, acc in results.items():
        print(f"{name}: {acc:.4f}")
    
    print("\nEvaluation complete. Confusion matrices saved as PNG images.")

if __name__ == "__main__":
    main()
