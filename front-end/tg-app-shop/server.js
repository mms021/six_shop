import http from 'http';
import { fileURLToPath } from 'url';
import { dirname, join, extname } from 'path';
import fs from 'fs/promises';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const PORT = 3478;
const distDir = join(__dirname, 'dist');

// Список разрешенных доменов (включая все поддомены)
const allowedOrigins = [
    'https://t.me',
    'https://telegram.org',
    'https://telegram.me',
    'https://mms021-six-shop-8662.twc1.net',
    'http://mms021-six-shop-8662.twc1.net',
    'http://mms021-six-shop-8662.twc1.net:7770',
    'https://mms021-six-shop-8662.twc1.net:7770',
    'http://localhost:3478',
    'http://0.0.0.0:3478'
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
        // Устанавливаем базовые заголовки для всех ответов
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
        res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
        res.setHeader('Access-Control-Max-Age', '86400');
        res.setHeader('X-Frame-Options', 'ALLOW-FROM https://t.me/');
        res.setHeader('Content-Security-Policy', "frame-ancestors 'self' https://t.me https://*.telegram.org https://*.telegram.me");

        // Обработка preflight запросов
        if (req.method === 'OPTIONS') {
            res.writeHead(204);
            res.end();
            return;
        }

        // Логируем запрос
        console.log(`${new Date().toISOString()} - ${req.method} ${req.url}`);

        let filePath = join(distDir, req.url === '/' ? 'index.html' : decodeURIComponent(req.url));
        const ext = extname(filePath);

        try {
            const content = await fs.readFile(filePath);
            res.writeHead(200, {
                'Content-Type': mimeTypes[ext] || 'application/octet-stream',
                'Cache-Control': 'public, max-age=31536000'
            });
            res.end(content);
        } catch (err) {
            if (err.code === 'ENOENT') {
                // Для SPA всегда возвращаем index.html при 404
                const indexContent = await fs.readFile(join(distDir, 'index.html'));
                res.writeHead(200, { 'Content-Type': 'text/html' });
                res.end(indexContent);
            } else {
                throw err;
            }
        }
    } catch (err) {
        console.error('Ошибка:', err);
        res.writeHead(500);
        res.end('Internal Server Error');
    }
});

// Проверяем существование dist директории и запускаем сервер
async function start() {
    try {
        await fs.access(distDir);
        console.log('Директория dist найдена');
        
        server.listen(PORT, '0.0.0.0', () => {
            console.log(`Сервер запущен на порту ${PORT}`);
        });
    } catch (err) {
        console.error('Ошибка при запуске:', err);
        process.exit(1);
    }
}

start(); 