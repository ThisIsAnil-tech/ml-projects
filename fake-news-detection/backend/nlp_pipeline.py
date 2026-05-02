import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import pickle
import os

class NLPPipeline:
    def __init__(self, max_features=5000):
        self.max_features = max_features
        self.bow_vectorizer = CountVectorizer(max_features=self.max_features, stop_words='english')
        self.tfidf_vectorizer = TfidfVectorizer(max_features=self.max_features, stop_words='english')

    def clean_text(self, text):
        if not isinstance(text, str):
            return ""
        text = text.lower()
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        return text

    def fit_transform(self, texts, method='tfidf'):
        cleaned_texts = [self.clean_text(t) for t in texts]
        if method == 'bow':
            return self.bow_vectorizer.fit_transform(cleaned_texts)
        elif method == 'tfidf':
            return self.tfidf_vectorizer.fit_transform(cleaned_texts)
        else:
            raise ValueError("Method must be 'bow' or 'tfidf'")

    def transform(self, texts, method='tfidf'):
        cleaned_texts = [self.clean_text(t) for t in texts]
        if method == 'bow':
            return self.bow_vectorizer.transform(cleaned_texts)
        elif method == 'tfidf':
            return self.tfidf_vectorizer.transform(cleaned_texts)
        else:
            raise ValueError("Method must be 'bow' or 'tfidf'")

    def save_vectorizers(self, save_dir):
        os.makedirs(save_dir, exist_ok=True)
        with open(os.path.join(save_dir, 'bow_vectorizer.pkl'), 'wb') as f:
            pickle.dump(self.bow_vectorizer, f)
        with open(os.path.join(save_dir, 'tfidf_vectorizer.pkl'), 'wb') as f:
            pickle.dump(self.tfidf_vectorizer, f)

    def load_vectorizers(self, save_dir):
        with open(os.path.join(save_dir, 'bow_vectorizer.pkl'), 'rb') as f:
            self.bow_vectorizer = pickle.load(f)
        with open(os.path.join(save_dir, 'tfidf_vectorizer.pkl'), 'rb') as f:
            self.tfidf_vectorizer = pickle.load(f)
