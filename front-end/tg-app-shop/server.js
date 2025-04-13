import http from 'http';
import { fileURLToPath } from 'url';
import { dirname, join, extname } from 'path';
import fs from 'fs/promises';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const PORT = 3478;
const distDir = join(__dirname, 'dist');

// Список разрешенных доменов
const allowedOrigins = [
    'https://t.me',
    'https://telegram.org',
    'https://telegram.me',
    'https://mms021-six-shop-8662.twc1.net'
];

// Добавляем определение mimeTypes
const mimeTypes = {
    '.html': 'text/html',
    '.js': 'text/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon',
    '.woff': 'application/font-woff',
    '.woff2': 'application/font-woff2',
    '.ttf': 'application/font-ttf',
    '.eot': 'application/vnd.ms-fontobject',
    '.otf': 'application/font-otf',
    '.wasm': 'application/wasm'
};

const server = http.createServer(async (req, res) => {
    try {
        // Добавляем CORS заголовки
        const origin = req.headers.origin;
        if (origin && allowedOrigins.includes(origin)) {
            res.setHeader('Access-Control-Allow-Origin', '*');  // Разрешаем все origins для Telegram
            res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
            res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
            res.setHeader('Access-Control-Max-Age', '86400');
        }

        // Обработка preflight запросов
        if (req.method === 'OPTIONS') {
            res.writeHead(204);
            res.end();
            return;
        }

        let filePath = join(distDir, req.url === '/' ? 'index.html' : decodeURIComponent(req.url));
        
        // Получаем расширение файла
        const ext = extname(filePath);
        
        try {
            const content = await fs.readFile(filePath);
            res.writeHead(200, {
                'Content-Type': mimeTypes[ext] || 'application/octet-stream',
                'Cache-Control': 'public, max-age=31536000',
                'X-Frame-Options': 'ALLOW-FROM https://t.me/',
                'Content-Security-Policy': "frame-ancestors 'self' https://t.me https://*.telegram.org https://*.telegram.me",
                'Access-Control-Allow-Origin': '*'  // Добавляем для всех ответов
            });
            res.end(content);
        } catch (err) {
            // Если файл не найден, возвращаем index.html
            if (err.code === 'ENOENT') {
                const indexContent = await fs.readFile(join(distDir, 'index.html'));
                res.writeHead(200, { 
                    'Content-Type': 'text/html',
                    'X-Frame-Options': 'ALLOW-FROM https://t.me/',
                    'Content-Security-Policy': "frame-ancestors 'self' https://t.me https://*.telegram.org https://*.telegram.me",
                    'Access-Control-Allow-Origin': '*'  // Добавляем для всех ответов
                });
                res.end(indexContent);
            } else {
                throw err;
            }
        }
    } catch (err) {
        console.error('Ошибка:', err);
        res.writeHead(500);
        res.end('Внутренняя ошибка сервера');
    }
});

// Проверяем существование dist директории
async function checkDistDirectory() {
    try {
        await fs.access(distDir);
        console.log('Директория dist найдена');
    } catch (err) {
        console.error('Ошибка: директория dist не найдена');
        process.exit(1);
    }
}

// Упрощенная функция запуска сервера
function startServer() {
    server.listen(PORT, '0.0.0.0', () => {
        console.log(`Сервер запущен на порту ${PORT}`);
    }).on('error', (err) => {
        console.error('Ошибка при запуске сервера:', err);
        process.exit(1);
    });
}

// Запускаем сервер
checkDistDirectory()
    .then(() => startServer())
    .catch(err => {
        console.error('Ошибка при запуске сервера:', err);
        process.exit(1);
    }); 