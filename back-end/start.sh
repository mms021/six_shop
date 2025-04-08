#!/bin/bash
set -e

echo "Запуск основного сервера..."
python main.py &
MAIN_PID=$!

# Проверка, что сервер запустился и доступен
echo "Ожидание запуска сервера..."
MAX_RETRIES=30
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -s http://localhost:7770/health 2>&1 > /dev/null || curl -s http://localhost:7770/ 2>&1 > /dev/null; then
        echo "Сервер успешно запущен!"
        break
    fi
    
    echo "Ожидание запуска сервера (попытка $RETRY_COUNT из $MAX_RETRIES)..."
    RETRY_COUNT=$((RETRY_COUNT+1))
    sleep 2
done

# Запускаем импорт продуктов в отдельном процессе
echo "Запуск импорта продуктов..."
python importProducts.py &
IMPORT_PID=$!

# Логирование информации о запущенных процессах
echo "Основной процесс PID: $MAIN_PID"
echo "Импорт продуктов PID: $IMPORT_PID"

# Ожидаем завершения основного приложения
# При завершении основного процесса скрипт также завершится
wait $MAIN_PID