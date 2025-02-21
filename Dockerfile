FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt update && apt install -y cron

COPY crontab /etc/cron.d/retrain-cron

RUN chmod 0644 /etc/cron.d/retrain-cron

RUN crontab /etc/cron.d/retrain-cron

CMD service cron start && python app.py
