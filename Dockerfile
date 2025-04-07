FROM python:3.10

WORKDIR /app

COPY bot/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY bot/ .

CMD ["python", "bot.py"] 