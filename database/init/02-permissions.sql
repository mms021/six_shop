-- Устанавливаем права доступа
GRANT USAGE ON SCHEMA tg_shop TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA tg_shop TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA tg_shop TO postgres;

-- Устанавливаем права по умолчанию для новых объектов
ALTER DEFAULT PRIVILEGES IN SCHEMA tg_shop
GRANT ALL PRIVILEGES ON TABLES TO postgres;

ALTER DEFAULT PRIVILEGES IN SCHEMA tg_shop
GRANT ALL PRIVILEGES ON SEQUENCES TO postgres; 