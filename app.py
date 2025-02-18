import re
import mysql.connector
import joblib
import pandas as pd
from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host='db',
        user='user',
        password='password',
        database='twitter_db'
    )


def clean_text(text):
    text = text.lower()  # Mettre en minuscule
    text = re.sub(r'[^\w\s]', '', text)
    return text


def train_model():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT text, positive, negative FROM tweets")
    data = cursor.fetchall()
    conn.close()


texts = [clean_text(row[0]) for row in data]
labels = [1 if row[1] == 1 else 0 for row in data]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

model = LogisticRegression()
model.fit(X, labels)

joblib.dump(model, 'sentiment_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')
try:
    model = joblib.load('sentiment_model.pkl')
    vectorizer = joblib.load('vectorizer.pkl')
except:
    train_model()
    model = joblib.load('sentiment_model.pkl')
    vectorizer = joblib.load('vectorizer.pkl')


@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    data = request.get_json()
    tweets = data.get("tweets", [])

    if not tweets or not isinstance(tweets, list):
        return jsonify({"error": "Invalid input"}), 400

    processed_tweets = [clean_text(tweet) for tweet in tweets]
    tweet_vectors = vectorizer.transform(processed_tweets)
    scores = model.predict_proba(tweet_vectors)[:, 1] * 2 - 1  # Scale between -1 and 1

    response = {tweet: float(score) for tweet, score in zip(tweets, scores)}
    return jsonify(response)
if __name__ == '__main__':
    app.run()
