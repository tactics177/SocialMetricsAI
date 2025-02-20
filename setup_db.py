import mysql.connector
import time

while True:
    try:
        db = mysql.connector.connect(
            host="mysql",
            user="root",
            password="root"
        )
        break
    except mysql.connector.Error:
        print("Waiting for MySQL to start...")
        time.sleep(5)

cursor = db.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS sentiment_analysis;")
cursor.execute("USE sentiment_analysis;")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tweets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT NOT NULL,
    positive TINYINT(1),
    negative TINYINT(1)
);
""")

cursor.execute("SELECT COUNT(*) FROM tweets;")
count = cursor.fetchone()[0]

if count == 0:
    sample_data = [
        # Strongly positive
        ("I love this!", 1, 0),
        ("Amazing experience!", 1, 0),
        ("Best service ever!", 1, 0),
        ("Highly recommend!", 1, 0),
        ("Totally worth it!", 1, 0),
        ("Fantastic product!", 1, 0),
        ("Life-changing!", 1, 0),
        ("Super happy with this!", 1, 0),
        ("Exceeded my expectations!", 1, 0),
        ("Absolutely wonderful!", 1, 0),
        ("Couldn't be happier!", 1, 0),
        ("This is perfection!", 1, 0),
        ("10/10 would buy again!", 1, 0),

        # Strongly negative
        ("This is terrible.", 0, 1),
        ("Absolutely horrible!", 0, 1),
        ("I regret buying this.", 0, 1),
        ("Worst service ever!", 0, 1),
        ("This ruined my day.", 0, 1),
        ("Total waste of money.", 0, 1),
        ("Horrible experience!", 0, 1),
        ("Completely disappointed.", 0, 1),
        ("Awful customer support.", 0, 1),
        ("I absolutely hate this!", 0, 1),
        ("I can't believe how bad this is!", 0, 1),
        ("Disgusting!", 0, 1),
        ("Would not recommend.", 0, 1),

        # Neutral / Mixed
        ("Not bad, but not great.", 0, 0),
        ("It's okay, not amazing.", 0, 0),
        ("Could be better.", 0, 0),
        ("Meh, it's fine.", 0, 0),
        ("Some good, some bad.", 0, 0),
        ("Nothing special.", 0, 0),
        ("Mixed feelings about this.", 0, 0),
        ("An average experience.", 0, 0),
        ("Not sure how I feel.", 0, 0),

        # Mildly positive
        ("Pretty good overall.", 1, 0),
        ("Liked it!", 1, 0),
        ("Nice but not perfect.", 1, 0),
        ("Decent for the price.", 1, 0),
        ("Quite enjoyable.", 1, 0),
        ("I might recommend it.", 1, 0),

        # Mildly negative
        ("Not great.", 0, 1),
        ("Could have been better.", 0, 1),
        ("A little disappointing.", 0, 1),
        ("Expected more.", 0, 1),
        ("Not what I hoped for.", 0, 1),
        ("Wouldn't buy again.", 0, 1),
        ("Felt a bit off.", 0, 1)
    ]

    cursor.executemany("INSERT INTO tweets (text, positive, negative) VALUES (%s, %s, %s);", sample_data)
    print("Sample data inserted.")

db.commit()
db.close()
print("Database setup complete!")
