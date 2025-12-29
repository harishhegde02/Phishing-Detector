
import pandas as pd
import joblib
import os
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.pipeline import Pipeline

def train_scalable_model():
    """
    Trains a scalable model (SGDClassifier) on the processed external dataset.
    Uses SGD (Stochastic Gradient Descent) which is efficient for large datasets.
    """
    data_dir = 'data/processed'
    models_dir = 'models'
    os.makedirs(models_dir, exist_ok=True)

    print("Loading valid/test data for evaluation dimensions...")
    # Load validation data first to get dimensions/labels correct if needed, 
    # but mainly we load train data.
    
    train_path = os.path.join(data_dir, 'train_ext.csv')
    val_path = os.path.join(data_dir, 'val_ext.csv')
    
    if not os.path.exists(train_path):
        print(f"Training data not found at {train_path}")
        return

    print(f"Loading training data from {train_path}...")
    # Read in chunks if necessary, but 1M rows with just text/labels might fit in 16GB RAM.
    # Let's try loading full DF first. If memory error, we switch to chunking.
    try:
        train_df = pd.read_csv(train_path)
        val_df = pd.read_csv(val_path)
        print(f"Training samples: {len(train_df)}")
        print(f"Validation samples: {len(val_df)}")
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # Prepare features and labels
    X_train = train_df['text'].fillna('')
    y_train = train_df[['urgency', 'authority', 'fear', 'impersonation']]
    
    X_val = val_df['text'].fillna('')
    y_val = val_df[['urgency', 'authority', 'fear', 'impersonation']]

    print("Vectorizing data (TF-IDF)...")
    # Limit max_features to keep memory usage reasonable, but high enough for variety
    vectorizer = TfidfVectorizer(max_features=20000, ngram_range=(1, 2), stop_words='english')
    X_train_vec = vectorizer.fit_transform(X_train)
    X_val_vec = vectorizer.transform(X_val)
    print(f"Feature matrix shape: {X_train_vec.shape}")

    print("Training SGDClassifier (OneVsRest)...")
    start_time = time.time()
    
    # SGDClassifier with 'log_loss' is equivalent to Logistic Regression roughly, but faster.
    # 'hinge' gives SVM. 'modified_huber' is robust.
    # Let's use 'log_loss' (formerly 'log') for probability outputs if needed, or 'hinge' for pure compat/speed.
    # The user's backend uses predict_proba, so we need 'log_loss' or 'modified_huber'.
    # 'log_loss' is the loss for logistic regression.
    clf = OneVsRestClassifier(SGDClassifier(loss='log_loss', random_state=42, n_jobs=-1, max_iter=1000, tol=1e-3))
    
    clf.fit(X_train_vec, y_train)
    
    print(f"Training completed in {time.time() - start_time:.2f} seconds.")

    print("\nEvaluating on Validation Set:")
    y_pred = clf.predict(X_val_vec)
    
    print("Accuracy Score:", accuracy_score(y_val, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_val, y_pred, target_names=['Urgency', 'Authority', 'Fear', 'Impersonation']))

    # Save models
    print("Saving model artifacts...")
    joblib.dump(vectorizer, os.path.join(models_dir, 'vectorizer_scalable.joblib'))
    joblib.dump(clf, os.path.join(models_dir, 'model_scalable.joblib'))
    print(f"Saved to {models_dir}")

if __name__ == "__main__":
    train_scalable_model()
