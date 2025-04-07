python main.py &
MAIN_PID=$!

# Ждем, пока сервер запустится
echo "Ожидание запуска сервера..."
sleep 10

# Запускаем импорт продуктов
echo "Запуск импорта продуктов..."
python importProducts.py

# Ждем завершения основного приложения
wait $MAIN_PID