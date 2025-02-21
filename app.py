from flask import Flask, request, jsonify
import mysql.connector
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import time

app = Flask(__name__)


def get_db_connection():
    mysql_host = os.getenv("MYSQL_HOST", "localhost") if os.getenv("FLASK_ENV") == "development" else "mysql"

    while True:
        try:
            db = mysql.connector.connect(
                host=mysql_host,
                user=os.getenv("MYSQL_USER", "root"),
                password=os.getenv("MYSQL_PASSWORD", "root"),
                database=os.getenv("MYSQL_DATABASE", "sentiment_analysis")
            )
            print("Connected to MySQL!")
            return db
        except mysql.connector.Error:
            print("Waiting for MySQL to be ready...")
            time.sleep(5)


def train_model():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT text, positive FROM tweets")
    data = cursor.fetchall()
    db.close()

    if not data:
        return None, None

    df = pd.DataFrame(data, columns=['text', 'positive'])

    vectorizer = TfidfVectorizer(stop_words='english', max_features=500)
    X = vectorizer.fit_transform(df['text']).toarray()
    y = df['positive'].values

    model = LogisticRegression(max_iter=500, class_weight='balanced')
    model.fit(X, y)

    return model, vectorizer


model, vectorizer = train_model()


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    tweets = data.get("tweets", [])

    if not tweets:
        return jsonify({"error": "No tweets provided"}), 400

    tweet_vectors = vectorizer.transform(tweets).toarray()
    probabilities = model.predict_proba(tweet_vectors)[:, 1]

    scores = {tweet: round(prob * 2 - 1, 2) for tweet, prob in zip(tweets, probabilities)}
    return jsonify(scores)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
