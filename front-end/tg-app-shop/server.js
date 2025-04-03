const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3478;

const server = http.createServer((req, res) => {
  // Устанавливаем базовую директорию для статических файлов
  const publicDir = path.join(__dirname, 'public');
  
  // Определяем путь к файлу
  let filePath = path.join(publicDir, req.url === '/' ? 'index.html' : req.url);
  
  // Получаем расширение файла
  const extname = path.extname(filePath);
  
  // Устанавливаем content-type в зависимости от расширения
  const contentType = {
    '.html': 'text/html',
    '.js': 'text/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpg',
    '.gif': 'image/gif',
  }[extname] || 'text/plain';
  
  // Проверяем существование файла
  fs.readFile(filePath, (err, content) => {
    if (err) {
      if (err.code === 'ENOENT') {
        // Файл не найден
        fs.readFile(path.join(publicDir, '404.html'), (err, content) => {
          res.writeHead(404, { 'Content-Type': 'text/html' });
          res.end(content || 'Страница не найдена', 'utf-8');
        });
      } else {
        // Другая ошибка сервера
        res.writeHead(500);
        res.end(`Ошибка сервера: ${err.code}`);
      }
    } else {
      // Успешный ответ
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content, 'utf-8');
    }
  });
});

server.listen(PORT, () => {
  console.log(`Сервер запущен на порту ${PORT}`);
}); 