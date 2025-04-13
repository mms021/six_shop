import http from 'http';
import { fileURLToPath } from 'url';
import { dirname, join, extname } from 'path';
import fs from 'fs/promises';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const PORT = 3478;

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
        const distDir = join(__dirname, 'dist');
        let filePath = join(distDir, req.url === '/' ? 'index.html' : decodeURIComponent(req.url));
        
        // Получаем расширение файла
        const ext = extname(filePath);
        
        try {
            const content = await fs.readFile(filePath);
            res.writeHead(200, {
                'Content-Type': mimeTypes[ext] || 'application/octet-stream',
                'Cache-Control': 'public, max-age=31536000' // кэширование на 1 год для статических файлов
            });
            res.end(content);
        } catch (err) {
            // Если файл не найден, возвращаем index.html
            if (err.code === 'ENOENT') {
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
        res.end('Внутренняя ошибка сервера');
    }
});

server.listen(PORT, '0.0.0.0', () => {
    console.log(`Сервер запущен на порту ${PORT}`);
}); 