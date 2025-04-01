FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x start.sh

# Установка cron
RUN apt-get update && apt-get install -y cron

# Копирование скрипта и добавление задания в кронтаб
COPY importProducts.py /app/importProducts.py
RUN echo "0 18 * * * python /app/importProducts.py" >> /etc/crontab

EXPOSE 7770

# Запуск cron в фоновом режиме
CMD cron && ./start.sh 