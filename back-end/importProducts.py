from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2 import service_account
import asyncio
import aiohttp
import ssl
import certifi
import os
from dotenv import load_dotenv
from models import async_session, Categori, init_db, ProductVariants, Products, ProductImage
from sqlalchemy import select, update
from urllib.parse import urlparse, quote
import tempfile
import json
import sys

# Загружаем переменные окружения из .env файла
load_dotenv()

# Настройки доступа
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Создаем временный файл с учетными данными из переменной окружения
def get_credentials_file():
    """Создает временный файл с учетными данными из переменной окружения"""
    credentials_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_json:
        raise ValueError("Переменная GOOGLE_APPLICATION_CREDENTIALS не установлена")
        
    # Создаем временный файл
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
    try:
        # Записываем JSON в файл
        with open(temp_file.name, 'w') as f:
            f.write(credentials_json)
        return temp_file.name
    except Exception as e:
        os.unlink(temp_file.name)  # Удаляем файл в случае ошибки
        raise e

CREDENTIALS_FILE = get_credentials_file()

# Настройки для изображений
IMAGES_DIR = 'static/categories'
os.makedirs(IMAGES_DIR, exist_ok=True)

PRODUCTS_DIR = 'static/products'
os.makedirs(PRODUCTS_DIR, exist_ok=True)

async def download_image(session, url, category_name):
    """Загрузка изображения с Яндекс.Диска"""
    try:
        # Проверяем, является ли ссылка ссылкой на Яндекс.Диск
        if 'disk.yandex.ru' in url:
            try:
                # Кодируем URL для безопасной передачи
                encoded_url = quote(url, safe=':/?=')
                
                # Формируем прямую ссылку на скачивание
                download_url = f"https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={encoded_url}"
                
                print(f"Getting download link from: {download_url}")
                
                # Получаем прямую ссылку на файл
                async with session.get(download_url, ssl=False) as response:
                    if response.status == 200:
                        data = await response.json()
                        direct_url = data.get('href')
                        if not direct_url:
                            print("No direct URL in response")
                            return None
                            
                        print(f"Got direct URL: {direct_url}")
                        
                        # Скачиваем файл по прямой ссылке
                        async with session.get(direct_url, ssl=False) as file_response:
                            if file_response.status == 200:
                                # Получаем оригинальное имя файла из заголовков
                                content_disposition = file_response.headers.get('Content-Disposition', '')
                                original_filename = content_disposition.split('filename=')[-1].strip('"')
                                file_extension = os.path.splitext(original_filename)[-1] or '.jpg'
                                
                                # Формируем безопасное имя файла
                                safe_category_name = "".join(c for c in category_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                                filename = f"{safe_category_name}{file_extension}"
                                filepath = os.path.join(IMAGES_DIR, filename)
                                
                                # Сохраняем файл
                                content = await file_response.read()
                                with open(filepath, 'wb') as f:
                                    f.write(content)
                                
                                print(f"Successfully saved image to: {filepath}")
                                return f"/static/categories/{filename}"
                            else:
                                print(f"Failed to download file. Status: {file_response.status}")
                                return None
                    else:
                        print(f"Failed to get download link. Status: {response.status}")
                        return None
                        
            except Exception as inner_e:
                print(f"Error during download process: {inner_e}")
                return None
                
        return url
    except Exception as e:
        print(f"Outer error: {e}")
        return None

def get_next_column(column, steps=1):
    """
    Получает следующий столбец Excel с учетом двойных букв.
    Например: 
    - get_next_column('Z', 1) вернет 'AA'
    - get_next_column('AA', 1) вернет 'AB'
    - get_next_column('A', 2) вернет 'C'
    """
    # Преобразуем столбец в число (A=1, B=2, ..., Z=26, AA=27, ...)
    col_num = 0
    for c in column:
        col_num = col_num * 26 + (ord(c) - ord('A') + 1)
    
    # Добавляем шаги
    col_num += steps
    
    # Преобразуем обратно в буквенное представление
    result = ""
    while col_num > 0:
        col_num, remainder = divmod(col_num - 1, 26)
        result = chr(ord('A') + remainder) + result
    
    return result

async def process_category_columns(sheet, spreadsheet_id, session, start_col='A'):
    """Обработка трех столбцов категорий"""
    # Обработка столбцов Excel с учетом двойных букв
    end_col = get_next_column(start_col, 2)  # Получаем столбец через 2 от начального
    range_name = f'Категории!{start_col}3:{end_col}20'
    
    try:
        result = sheet.values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()
        
        values = result.get('values', [])
        
        if not values or not values[0]:
            return False
        
        current_parent = None
        
        async with aiohttp.ClientSession() as http_session:
            for row in values:
                if not row or not row[0].strip():
                    continue
                
                category_name = row[0].strip()
                visibility = True if len(row) > 1 and row[1].strip().lower() == 'true' else False
                image_url = row[2].strip() if len(row) > 2 and row[2].strip() else ''
                
                # Загружаем изображение, если есть URL
                if image_url:
                    # Добавляем задержку перед каждым запросом к Яндекс.Диску
                    await asyncio.sleep(2)  # Задержка 2 секунды
                    downloaded_image_path = await download_image(http_session, image_url, category_name)
                    if downloaded_image_path:
                        image_url = downloaded_image_path
                    else:
                        # Если загрузка не удалась, делаем дополнительную попытку после увеличенной задержки
                        print(f"Retrying download for {category_name} after delay...")
                        await asyncio.sleep(5)  # Увеличенная задержка перед повторной попыткой
                        downloaded_image_path = await download_image(http_session, image_url, category_name)
                        if downloaded_image_path:
                            image_url = downloaded_image_path
                
                existing_category = await session.scalar(
                    select(Categori).where(Categori.name == category_name)
                )
                
                if current_parent is None:
                    if existing_category:
                        existing_category.visibility = visibility
                        existing_category.image_url = image_url
                        current_parent = existing_category
                        print(f"Updated main category: {category_name}")
                    else:
                        category = Categori(
                            name=category_name,
                            visibility=visibility,
                            image_url=image_url,
                            parent_id=None
                        )
                        session.add(category)
                        await session.flush()
                        current_parent = category
                        print(f"Added main category: {category_name}")
                else:
                    if existing_category:
                        existing_category.visibility = visibility
                        existing_category.image_url = image_url
                        existing_category.parent_id = current_parent.id
                        print(f"Updated subcategory: {category_name} under {current_parent.name}")
                    else:
                        subcategory = Categori(
                            name=category_name,
                            visibility=visibility,
                            image_url=image_url,
                            parent_id=current_parent.id
                        )
                        session.add(subcategory)
                        print(f"Added subcategory: {category_name} under {current_parent.name}")
        
        await session.commit()
        print("All categories imported successfully")
        return True
        
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return False

async def get_sheet_data():
    # Создаем учетные данные из файла service account
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES)

    # Создаем сервис
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()

    # ID таблицы
    SPREADSHEET_ID = '1cf06jIf5y8LHAjFtqtR2-vGSlDTKJGcysN-8vQ4jxTI'
    
    # Обрабатываем все группы столбцов
    async with async_session() as session:
        # Захардкоженные столбцы для импорта категорий
        category_columns = ['C', 'F', 'I', 'L', 'O', 'R', 'U', 'X']
        
        for col in category_columns:
            print(f"Обработка категорий из столбца {col}")
            await process_category_columns(
                sheet, 
                SPREADSHEET_ID, 
                session,
                col
            )
            
        await session.commit()
        print("All categories imported successfully")

async def process_sizes(session, product, size_str):
    """Обработка строки с размерами"""
    if not size_str:
        return
        
    if size_str.strip() == 'По запросу':
        product.description += '\nДоступные размеры можете уточнить по запросу'
        return
        
    # Разбиваем строку размеров по запятой и очищаем от пробелов
    sizes = [size.strip() for size in size_str.split(',') if size.strip()]

    
    
    for size in sizes:
        variant = ProductVariants(
            product_id=product.id,
            name=size
        )
        session.add(variant)

async def get_public_resources(session, public_key, path=""):
    """Получает список файлов из публичной папки Яндекс.Диска"""
    url = "https://cloud-api.yandex.net/v1/disk/public/resources"
    
    params = {
        "public_key": public_key,
        "path": path,
        "limit": 100
    }
    
    async with session.get(url, params=params, ssl=False) as response:
        if response.status == 200:
            return await response.json()
        else:
            print(f"Ошибка при получении списка файлов: {response.status}")
            print(await response.text())
            return None

async def get_download_link(session, public_key, path=""):
    """Получает прямую ссылку на скачивание файла"""
    url = "https://cloud-api.yandex.net/v1/disk/public/resources/download"
    
    params = {
        "public_key": public_key,
        "path": path
    }
    
    async with session.get(url, params=params, ssl=False) as response:
        if response.status == 200:
            data = await response.json()
            return data.get("href")
        else:
            print(f"Ошибка при получении ссылки на скачивание: {response.status}")
            print(await response.text())
            return None

async def download_file(session, download_url, product_id, idx):
    """Скачивает файл по прямой ссылке"""
    try:
        async with session.get(download_url, ssl=False) as response:
            if response.status == 200:
                # Получаем расширение файла из Content-Type или из URL
                content_type = response.headers.get('Content-Type', '')
                extension = '.jpg'  # По умолчанию
                
                if 'image/jpeg' in content_type:
                    extension = '.jpg'
                elif 'image/png' in content_type:
                    extension = '.png'
                elif 'image/gif' in content_type:
                    extension = '.gif'
                elif 'image/webp' in content_type:
                    extension = '.webp'
                
                # Формируем имя файла
                filename = f"{product_id}_{idx}{extension}"
                filepath = os.path.join(PRODUCTS_DIR, filename)
                
                # Сохраняем файл
                content = await response.read()
                with open(filepath, 'wb') as f:
                    f.write(content)
                
                print(f"Файл сохранен: {filepath}")
                return f"/static/products/{filename}"
            else:
                print(f"Ошибка при скачивании файла: {response.status}")
                return None
    except Exception as e:
        print(f"Ошибка при скачивании файла: {e}")
        return None

async def process_product_photos(session, product, photos_folder):
    """Обрабатывает фотографии продукта из папки Яндекс.Диска"""
    try:
        # Создаем HTTP-сессию для запросов к API
        async with aiohttp.ClientSession() as http_session:
            # Получаем список файлов из папки
            resources = await get_public_resources(http_session, photos_folder)
            
            if not resources:
                print(f"Не удалось получить ресурсы для {photos_folder}")
                return
            
            print(f"Получены данные о папке: {photos_folder}")
            print(f"Структура ответа: {list(resources.keys())}")
            
            # Если это папка, получаем список файлов
            if resources.get("_embedded", {}).get("items"):
                items = resources["_embedded"]["items"]
                print(f"Найдено {len(items)} элементов в папке")
                
                for idx, item in enumerate(items):
                    item_path = item.get("path", "").replace("disk:", "")
                    item_name = item.get("name", "")
                    item_type = item.get("type", "")
                    
                    print(f"Обрабатываем элемент {idx}: {item_name} (тип: {item_type})")
                    
                    if item_type == "file" and item.get("mime_type", "").startswith("image/"):
                        # Получаем ссылку на скачивание
                        download_url = await get_download_link(http_session, photos_folder, item_path)
                        
                        if download_url:
                            print(f"Скачивание {item_name}...")
                            image_path = await download_file(http_session, download_url, product.id, idx)
                            
                            if image_path:
                                product_image = ProductImage(
                                    product_id=product.id,
                                    image_url=image_path,
                                    is_main=(idx == 0)  # Первое фото будет главным
                                )
                                session.add(product_image)
                                print(f"Добавлено изображение {image_path} для продукта {product.id}")
            
            # Если это файл, скачиваем его
            elif resources.get("type") == "file" and resources.get("mime_type", "").startswith("image/"):
                item_path = resources.get("path", "").replace("disk:", "")
                download_url = await get_download_link(http_session, photos_folder, item_path)
                
                if download_url:
                    print(f"Скачивание одиночного файла...")
                    image_path = await download_file(http_session, download_url, product.id, 0)
                    
                    if image_path:
                        product_image = ProductImage(
                            product_id=product.id,
                            image_url=image_path,
                            is_main=True
                        )
                        session.add(product_image)
                        print(f"Добавлено изображение {image_path} для продукта {product.id}")
    
    except Exception as e:
        print(f"Ошибка при обработке фотографий: {e}")

async def process_products(sheet, spreadsheet_id, session):
    """Загрузка продуктов из таблицы"""
    range_name = 'База продуктов!C3:M'
    
    def clean_price(price_str):
        """Очищает строку цены от символов и преобразует в число"""
        if not price_str:
            return 0.0
        # Удаляем символ рубля, пробелы и неразрывные пробелы
        price_str = price_str.replace('р.', '').replace(' ', '').replace('\xa0', '')
        try:
            return float(price_str)
        except ValueError:
            print(f"Не удалось преобразовать цену: {price_str}")
            return 0.0

    try:
        result = sheet.values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()
        
        values = result.get('values', [])
        if not values:
            print("Нет данных о продуктах")
            return False
            
        async with aiohttp.ClientSession() as http_session:
            for row in values:
                if len(row) < 11:  # Проверяем, что есть все необходимые колонки
                    continue
                    
                try:
                    item_id = int(row[0]) if row[0] else None
                    name = row[1].strip()
                    brand = row[2].strip()
                    description = row[3].strip()
                    subcategory_name = row[5].strip()  # Пропускаем category (индекс 4)
                    price_old = clean_price(row[6]) if len(row) > 6 else 0.0
                    price_promo = clean_price(row[7]) if len(row) > 7 else 0.0
                    size_str = row[8].strip() if len(row) > 8 else ''
                    visibility = row[9].lower() == 'true' if len(row) > 9 else True
                    photos_folder = row[10].strip() if len(row) > 10 else ''
                    
                    # Находим категорию
                    category = await session.scalar(
                        select(Categori).where(Categori.name == subcategory_name)
                    )
                    
                    if not category:
                        print(f"Категория не найдена: {subcategory_name}")
                        continue
                    
                    # Получаем или создаем продукт
                    product = await session.scalar(
                        select(Products).where(Products.id == item_id)
                    ) if item_id else None
                    
                    if product:
                        # Обновляем существующий продукт
                        product.name = name
                        product.brend = brand
                        product.description = description
                        product.categori_id = category.id
                        product.price = price_promo
                        product.old_price = price_old
                        product.visibility = visibility
                    else:
                        # Создаем новый продукт
                        product = Products(
                            id=item_id,
                            name=name,
                            brend=brand,
                            description=description,
                            categori_id=category.id,
                            price=price_promo,
                            old_price=price_old,
                            visibility=visibility
                        )
                        session.add(product)
                        await session.flush()  # Получаем ID продукта
                    
                    # Обрабатываем размеры
                    if size_str:
                        await process_sizes(session, product, size_str)
                    
                    # Обрабатываем фотографии
                    if photos_folder:
                        await process_product_photos(session, product, photos_folder)
                    
                    await session.commit()
                    print(f"Обработан продукт: {name}")
                    
                except Exception as e:
                    print(f"Ошибка при обработке продукта: {e}")
                    await session.rollback()
                    continue
                
        return True
        
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return False

async def main():
    # Создаем учетные данные из файла service account
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES)

    # Создаем сервис
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()

    # ID таблицы
    SPREADSHEET_ID = '1cf06jIf5y8LHAjFtqtR2-vGSlDTKJGcysN-8vQ4jxTI'
    
    async with async_session() as session:
        print("Импорт категорий...")
        await get_sheet_data()
        print("Импорт продуктов...")
        await process_products(sheet, SPREADSHEET_ID, session)
        print("Импорт завершен")

    
    try:
        os.unlink(CREDENTIALS_FILE)
        print(f"Временный файл учетных данных удален: {CREDENTIALS_FILE}")
    except Exception as e:
        print(f"Ошибка при удалении временного файла: {e}")

if __name__ == "__main__":
    args = sys.argv
    print(args)
    if len(args) > 1 and args[1] == 'init':
        asyncio.run(init_db())
    asyncio.run(main())
    