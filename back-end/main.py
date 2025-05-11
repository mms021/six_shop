from contextlib import asynccontextmanager
import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, Header, HTTPException, Query, UploadFile, File, Form, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import hmac
import hashlib
from datetime import datetime, timedelta
import json
import shutil
import os
from fastapi.staticfiles import StaticFiles
from functools import wraps
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import init_db, ProductResponse, CategoryResponse, ProductDetailResponse, ProductListResponse, SortOrder, ProductFilter, async_session, Cart, CartItem, Products, ProductImage, ProductVariants, OrderStatus, User,  Reaction
import requests_db as rq




# Функция для получения сессии базы данных
async def get_async_session():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

BOT_TOKEN = os.getenv('TG_BOT_TOKEN')

FRONTEND_URL = os.getenv('FRONTEND_URL')
BACKEND_URL = os.getenv('BACKEND_URL')

@asynccontextmanager
async def lifespan(app_:FastAPI):
    await init_db()
    print('DB is ready')
    yield


app = FastAPI(title='Shop', lifespan=lifespan)

# Обновляем конфигурацию CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://t.me",
        "https://telegram.org",
        "https://telegram.me",
        #"https://mms021-flowshop-1-ce60.twc1.net",
        #"http://localhost:3478",
        #"http://0.0.0.0:3478",
        "*"  # Временно разрешаем все домены для отладки
    ],
    #allow_origin_regex="https?://.*",  # Разрешаем все домены через регулярное выражение
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Монтируем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

# Создаем директории если их нет
os.makedirs("static/products", exist_ok=True)
os.makedirs("static/categories", exist_ok=True)

def validate_telegram_data(init_data: str = Header(None)):
    if not init_data:
        raise HTTPException(status_code=401, detail="No Telegram data provided")
    
    # Разбираем init_data
    data_dict = dict(param.split('=') for param in init_data.split('&'))
    
    # Получаем hash для проверки
    received_hash = data_dict.pop('hash')
    
    # Сортируем оставшиеся параметры
    data_check_string = '\n'.join(f"{k}={v}" for k, v in sorted(data_dict.items()))
    
    # Создаем secret_key из токена бота
    secret_key = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
    
    # Вычисляем hash
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    
    if calculated_hash != received_hash:
        raise HTTPException(status_code=401, detail="Invalid Telegram data")

class UserData(BaseModel):
    tg_id: int
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None

class ProductAction(BaseModel):
    userId: int
    productId: int
    variantId: int | None = None

class OrderResponse(BaseModel):
    id: int
    status: str
    created_at: datetime
    items: List[dict]
    total: float
    name: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    comment: str | None = None

@app.get("/")
async def root():
    return {"message": "site"}



# Пользователь
@app.get("/api/users/{tg_id}")
async def get_user(tg_id: int, user_data: UserData, telegram_data: str = Header(None, alias="Telegram-Data")):
    validate_telegram_data(telegram_data)
    user = await rq.get_or_create_user(user_data.dict())
    return user


# Дашборд
@app.get("/api/products")
async def get_dashboard_products():
    products = await rq.get_products_all()
    return {
        "products": [
            {
                "id": product.id,
                "name": product.name,
                "productPrice": product.price,
                "productOldPrice": product.old_price,
                "image": product.image_url,
                "isLiked": product.is_liked,
                "isInCart": product.is_in_cart
            } for product in products
        ]
    }

# Товары категории
@app.get("/api/products/{cat_id}", response_model=ProductListResponse)
async def get_category_products(
    cat_id: int,
    page: int = 1,
    limit: int = 30,
    price_order: SortOrder | None = None,
    size: str | None = None,
    brand: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None
):
    offset = (page - 1) * limit
    filters = ProductFilter(
        price_order=price_order,
        size=size,
        brand=brand,
        min_price=min_price,
        max_price=max_price
    )
    products, total = await rq.get_products_by_category(cat_id, limit, offset, filters)
    
    return {
        "products": [
            {
                "id": product.id,
                "name": product.name,
                "productPrice": product.price,
                "productOldPrice": product.old_price,
                "productImages": [img.image_url for img in product.images],
                "isLiked": product.is_liked,
                "isInCart": product.is_in_cart,
                "brend": product.brend,
                "description": product.description
            } for product in products
        ],
        "total": total,
        "hasMore": total > (offset + limit)
    }

# Товар 
@app.get("/api/products/detail/{pr_id}", response_model=ProductDetailResponse)
async def get_detail_products(pr_id: int):
    product = await rq.get_products(pr_id)
    return {
        "productId": product.id,
        "productName": product.name,
        "productDescription": product.description,
        "productPrice": product.price,
        "productOldPrice": product.old_price,
        "productCategory": product.category,
        "productBrand": product.brend,
        "productImages": [
            {
                "id": img.id,
                "url": img.image_url,
                "isMain": img.is_main
            } for img in product.images
        ],
        "productsVariants": product.variants,
        "isLiked": product.is_liked,
        "isInCart": product.is_in_cart
    }

# Категории
@app.get("/api/categories")
async def get_categories():
    return await rq.get_categoris()




# Добавление в избранное
@app.post("/api/like")
async def add_to_like(
    product_data: ProductAction,
    telegram_data: str = Header(None, alias="Telegram-Data")
):
    validate_telegram_data(telegram_data)
    result = await rq.toggle_like(product_data.userId, product_data.productId)
    return {"success": True, "isLiked": result}

# Добавление в корзину
@app.post("/api/cart")
async def add_to_cart(
    product_data: ProductAction,
    telegram_data: str = Header(None, alias="Telegram-Data")
):
    validate_telegram_data(telegram_data)
    result = await rq.add_to_cart(
        product_data.userId, 
        product_data.productId,
        product_data.variantId
    )
    return {"success": True, "isInCart": True}

@app.get("/api/search")
async def search_products(
    q: str = Query(..., min_length=2),
    limit: int = 10
):
    products = await rq.search_products(q, limit)
    return {
        "suggestions": [
            {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "image": product.images[0].image_url if product.images else None,
                "category": product.category_name
            } for product in products
        ]
    }

# Декоратор для проверки прав администратора
def admin_required(func):
    @wraps(func)
    async def wrapper(*args, telegram_data: str = Header(None, alias="Telegram-Data"), **kwargs):
        if not telegram_data:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        validate_telegram_data(telegram_data)
        data_dict = dict(param.split('=') for param in telegram_data.split('&'))
        user_data = json.loads(data_dict.get('user', '{}'))
        
        if not user_data:
            raise HTTPException(status_code=401, detail="Unauthorized")
            
        user = await rq.get_user_by_tg_id(user_data.get('id'))
        if not user or not user.get('is_admin'):
            raise HTTPException(status_code=403, detail="Access denied")
            
        return await func(*args, telegram_data=telegram_data, **kwargs)
    return wrapper

# Теперь применяем декоратор ко всем админским эндпоинтам
@app.get("/api/admin/dashboard")
@admin_required
async def get_admin_dashboard(telegram_data: str = Header(None, alias="Telegram-Data")):
    return await rq.get_dashboard_stats()



# Создание товара
@app.post("/api/admin/products")
@admin_required
async def create_product(
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    old_price: float = Form(...),
    category_id: int = Form(...),
    brand: str = Form(None),
    variants: str = Form(None),  # JSON строка с вариантами
    images: List[UploadFile] = File(None),
    main_image_index: int = Form(0),
    telegram_data: str = Header(None, alias="Telegram-Data")
):
    if telegram_data:
        validate_telegram_data(telegram_data)
        
    try:
        # Сохраняем изображения
        image_paths = []
        if images:
            for image in images:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_extension = os.path.splitext(image.filename)[1]
                new_filename = f"{timestamp}{file_extension}"
                file_path = f"static/products/{new_filename}"
                
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(image.file, buffer)
                image_paths.append(f"/{file_path}")
        
        # Создаем продукт
        product = await rq.create_product(
            name=name,
            description=description,
            price=price,
            old_price=old_price,
            category_id=category_id,
            brand=brand,
            variants=variants,
            images=image_paths,
            main_image_index=main_image_index
        )
        
        return {"success": True, "product": product}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Обновление товара
@app.put("/api/admin/products/{product_id}")
@admin_required
async def update_product(
    product_id: int,
    name: str = Form(None),
    description: str = Form(None),
    price: float = Form(None),
    old_price: float = Form(None),
    category_id: int = Form(None),
    brand: str = Form(None),
    variants: str = Form(None),
    new_images: List[UploadFile] = File(None),
    main_image_index: int = Form(None),
    deleted_images: str = Form(None),  # JSON строка с ID удаляемых изображений
    telegram_data: str = Header(None, alias="Telegram-Data")
):
    if telegram_data:
        validate_telegram_data(telegram_data)
        
    try:
        # Сохраняем новые изображения
        new_image_paths = []
        if new_images:
            for image in new_images:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_extension = os.path.splitext(image.filename)[1]
                new_filename = f"{timestamp}{file_extension}"
                file_path = f"static/products/{new_filename}"
                
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(image.file, buffer)
                new_image_paths.append(f"/{file_path}")
        
        # Обновляем продукт
        product = await rq.update_product(
            product_id=product_id,
            name=name,
            description=description,
            price=price,
            old_price=old_price,
            category_id=category_id,
            brand=brand,
            variants=variants,
            new_images=new_image_paths,
            main_image_index=main_image_index,
            deleted_images=deleted_images
        )
        
        return {"success": True, "product": product}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Удаление товара
@app.delete("/api/admin/products/{product_id}")
async def delete_product(
    product_id: int,
    telegram_data: str = Header(None, alias="Telegram-Data")
):
    if telegram_data:
        validate_telegram_data(telegram_data)
        
    try:
        await rq.delete_product(product_id)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Получение списка товаров для админки
@app.get("/api/admin/products")
async def get_admin_products(
    page: int = 1,
    limit: int = 20,
    category_id: int = None,
    search: str = None,
    telegram_data: str = Header(None, alias="Telegram-Data")
):
    if telegram_data:
        validate_telegram_data(telegram_data)
        
    products = await rq.get_admin_products(
        page=page,
        limit=limit,
        category_id=category_id,
        search=search
    )
    return products

@app.get("/api/admin/test")
async def test():
    return {"success": True}



# Получение всех категорий с подкатегориями
@app.get("/api/admin/categories")
async def get_admin_categories(telegram_data: str = Header(None, alias="Telegram-Data")):
    validate_telegram_data(telegram_data)
    categories = await rq.get_categories_tree()
    return categories

# Создание/обновление категории
@app.post("/api/admin/categories")
@admin_required
async def create_or_update_category(
    category_id: int = None,
    name: str = Form(...),
    parent_id: int = Form(None),
    visibility: bool = Form(True),
    image: UploadFile = File(None),
    telegram_data: str = Header(None, alias="Telegram-Data")
):
    validate_telegram_data(telegram_data)
    
    try:
        image_path = None
        if image:
            # Сохраняем изображение
            file_path = f"static/categories/{image.filename}"
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            image_path = file_path
        
        category = await rq.create_or_update_category(
            category_id=category_id,
            name=name,
            parent_id=parent_id,
            visibility=visibility,
            image_url=image_path
        )
        
        return {"success": True, "id": category.id}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Удаление категории
@app.delete("/api/admin/categories/{category_id}")
@admin_required
async def delete_category(
    category_id: int,
    telegram_data: str = Header(None, alias="Telegram-Data")
):
    validate_telegram_data(telegram_data)
    
    try:
        await rq.delete_category(category_id)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/products/best")
async def get_best_products(
    limit: int = Query(10, ge=1, le=50),
    user_id: Optional[int] = Query(None),
    session: AsyncSession = Depends(get_async_session)
):
    """Получение лучших продуктов"""
    try:
        # Получаем продукты
        query = select(Products).where(Products.visibility == True).order_by(Products.id.desc()).limit(limit)
        result = await session.execute(query)
        products = result.scalars().all()
        
        # Преобразуем в список словарей
        products_list = []
        for product in products:
            # Получаем изображения продукта
            images_query = select(ProductImage).where(ProductImage.product_id == product.id)
            images_result = await session.execute(images_query)
            images = images_result.scalars().all()
            
            # Проверяем, есть ли реакция пользователя на продукт
            is_favorite = False
            if user_id:
                reaction_query = select(Reaction).where(
                    Reaction.user_id == user_id,
                    Reaction.product_id == product.id
                )
                reaction_result = await session.execute(reaction_query)
                reaction = reaction_result.scalar_one_or_none()
                is_favorite = reaction is not None
            
            # Добавляем продукт в список
            products_list.append({
                "id": product.id,
                "name": product.name,
                "productPrice": product.price,
                "productOldPrice": product.old_price,
                "image": images[0].image_url if images else None,
                "isFavorite": is_favorite
            })
        
        return products_list
    except Exception as e:
        print(f"Ошибка при получении лучших продуктов: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/products/{product_id}")
async def get_product(
    product_id: int,
    user_id: int = None,
    telegram_data: str = Header(None, alias="Telegram-Data")
):
    if telegram_data:
        validate_telegram_data(telegram_data)
    
    product = await rq.get_product_by_id(product_id, user_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/api/cart/items")
async def get_cart_items(
    user_id: int,
    telegram_data: str = Header(None, alias="Telegram-Data")
):
    if telegram_data:
        validate_telegram_data(telegram_data)
    return await rq.get_cart_items(user_id)

@app.get("/api/orders/history")
async def get_order_history(
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        # Получаем все заказы пользователя
        orders = await session.execute(
            select(Cart)
            .where(Cart.user_id == user_id)
            .where(Cart.is_ordered == True)
            .order_by(Cart.created_at.desc())
        )
        orders = orders.scalars().all()
        
        # Получаем данные пользователя
        user = await session.scalar(
            select(User).where(User.id == user_id)
        )
        
        result = []
        for order in orders:
            # Получаем товары заказа
            items_query = await session.execute(
                select(
                    CartItem, 
                    Products,
                    ProductVariants,
                    ProductImage
                )
                .join(Products, CartItem.product_id == Products.id)
                .outerjoin(ProductVariants, CartItem.variants_id == ProductVariants.id)
                .outerjoin(ProductImage, ProductImage.product_id == Products.id)
                .where(CartItem.cart_id == order.id)
            )
            items = items_query.all()
            
            order_items = []
            total = 0
            
            for item, product, variant, image in items:
                item_data = {
                    "id": item.id,
                    "name": product.name,
                    "variant": variant.name if variant else None,
                    "price": product.price,
                    "image": image.image_url if image else None
                }
                order_items.append(item_data)
                total += product.price
            
            order_data = OrderResponse(
                id=order.id,
                status=order.status,
                created_at=order.created_at,
                items=order_items,
                total=total,
                name=user.name,
                phone=user.phone,
                email=user.email,
                address=user.address,
                comment=user.comment
            )
            
            result.append(order_data.dict())
            
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/favorites")
async def get_favorites(
    user_id: int,
    telegram_data: str = Header(None, alias="Telegram-Data")
):
    if telegram_data:
        validate_telegram_data(telegram_data)
    return await rq.get_favorite_products(user_id)

@app.get("/api/categories/{category_id}")
async def get_category_data(
    category_id: int,
    user_id: int = None,
    telegram_data: str = Header(None, alias="Telegram-Data")
):
    if telegram_data:
        validate_telegram_data(telegram_data)
    
    data = await rq.get_category_data(category_id, user_id)
    if not data:
        raise HTTPException(status_code=404, detail="Category not found")
    return data

# Загрузка файла
@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...),
    folder: str = "products",  # products или categories
    telegram_data: str = Header(None, alias="Telegram-Data")
):
    if telegram_data:
        validate_telegram_data(telegram_data)
        
    try:
        # Создаем уникальное имя файла
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = os.path.splitext(file.filename)[1]
        new_filename = f"{timestamp}{file_extension}"
        
        # Путь для сохранения
        file_path = f"static/{folder}/{new_filename}"
        
        # Сохраняем файл
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Возвращаем путь к файлу
        return {
            "success": True,
            "file_path": f"/{file_path}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Получение дерева категорий
@app.get("/api/admin/categories/tree")
@admin_required
async def get_categories_tree(telegram_data: str = Header(None, alias="Telegram-Data")):
    return await rq.get_categories_tree()

# Создание категории
@app.post("/api/admin/categories")
@admin_required
async def create_category(
    name: str = Form(...),
    parent_id: int = Form(None),
    image: UploadFile = File(None),
    telegram_data: str = Header(None, alias="Telegram-Data")
):
    if telegram_data:
        validate_telegram_data(telegram_data)
        
    try:
        image_path = None
        if image:
            # Сохраняем изображение
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_extension = os.path.splitext(image.filename)[1]
            new_filename = f"{timestamp}{file_extension}"
            file_path = f"static/categories/{new_filename}"
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            image_path = f"/{file_path}"
        
        category = await rq.create_category(
            name=name,
            parent_id=parent_id,
            image_url=image_path
        )
        
        return {"success": True, "category": category}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Обновление категории
@app.put("/api/admin/categories/{category_id}")
@admin_required
async def update_category(
    category_id: int,
    name: str = Form(...),
    parent_id: int = Form(None),
    image: UploadFile = File(None),
    telegram_data: str = Header(None, alias="Telegram-Data")
):
    if telegram_data:
        validate_telegram_data(telegram_data)
        
    try:
        image_path = None
        if image:
            # Сохраняем новое изображение
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_extension = os.path.splitext(image.filename)[1]
            new_filename = f"{timestamp}{file_extension}"
            file_path = f"static/categories/{new_filename}"
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            image_path = f"/{file_path}"
        
        category = await rq.update_category(
            category_id=category_id,
            name=name,
            parent_id=parent_id,
            image_url=image_path
        )
        
        return {"success": True, "category": category}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Удаление категории
@app.delete("/api/admin/categories/{category_id}")
@admin_required
async def delete_category(
    category_id: int,
    telegram_data: str = Header(None, alias="Telegram-Data")
):
    validate_telegram_data(telegram_data)
    
    try:
        await rq.delete_category(category_id)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/admin/statistics")
@admin_required
async def get_statistics(telegram_data: str = Header(None, alias="Telegram-Data")):
    return await rq.get_admin_statistics()

@app.get("/api/admin/orders")
@admin_required
async def get_admin_orders(
    page: int = 1,
    limit: int = 20,
    status: str = None,
    telegram_data: str = Header(None, alias="Telegram-Data")
):
    if telegram_data:
        validate_telegram_data(telegram_data)
    return await rq.get_admin_orders(page=page, limit=limit, status=status)

@app.get("/api/admin/products/list")
@admin_required
async def get_admin_products_list(
    page: int = 1,
    limit: int = 20,
    search: str = None,
    category_id: int = None,
    telegram_data: str = Header(None, alias="Telegram-Data")
):
    if telegram_data:
        validate_telegram_data(telegram_data)
    return await rq.get_admin_products_list(page=page, limit=limit, search=search, category_id=category_id)

@app.put("/api/admin/products/{product_id}/visibility")
@admin_required
async def toggle_product_visibility(
    product_id: int,
    telegram_data: str = Header(None, alias="Telegram-Data")
):
    if telegram_data:
        validate_telegram_data(telegram_data)
    return await rq.toggle_product_visibility(product_id)

@app.post("/api/concierge/request")
async def create_concierge_request(
    name: str = Form(...),
    contact: str = Form(...),
    product_link: str = Form(None),
    details: str = Form(...),
    telegram_data: str = Header(None, alias="Telegram-Data")
):
    if telegram_data:
        validate_telegram_data(telegram_data)
    return await rq.create_concierge_request(name, contact, product_link, details)

@app.get("/api/admin/concierge/requests")
@admin_required
async def get_concierge_requests(
    page: int = 1,
    limit: int = 20,
    status: str = None,
    telegram_data: str = Header(None, alias="Telegram-Data")
):
    if telegram_data:
        validate_telegram_data(telegram_data)
    return await rq.get_concierge_requests(page=page, limit=limit, status=status)

@app.put("/api/admin/concierge/requests/{request_id}/status")
@admin_required
async def update_concierge_request_status(
    request_id: int,
    status: str = Form(...),
    telegram_data: str = Header(None, alias="Telegram-Data")
):
    if telegram_data:
        validate_telegram_data(telegram_data)
    return await rq.update_concierge_request_status(request_id, status)

@app.get("/api/user/status")
async def get_user_status(telegram_data: str = Header(None, alias="Telegram-Data")):
    if telegram_data:
        validate_telegram_data(telegram_data)
        # Получаем данные пользователя из telegram_data
        data_dict = dict(param.split('=') for param in telegram_data.split('&'))
        user_data = json.loads(data_dict.get('user', '{}'))
        if user_data:
            user = await rq.get_user_by_tg_id(user_data.get('id'))
            return {"is_admin": user.get('is_admin', False) if user else False}
    return {"is_admin": False}

@app.post("/api/orders/checkout")
async def checkout_order(
    data: dict,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        # Получаем корзину
        cart = await session.scalar(
            select(Cart)
            .where(Cart.id.in_(data['cartId']))
            .where(Cart.is_ordered == False)
        )
        
        if not cart:
            raise HTTPException(status_code=404, detail="Корзина не найдена")
            
        # Получаем пользователя
        user = await session.scalar(
            select(User).where(User.id == cart.user_id)
        )
        
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
            
        # Обновляем данные пользователя
        user.name = data['userData']['name']
        user.phone = data['userData']['phone']
        user.email = data['userData']['email']
        user.address = data['userData']['address']
        user.comment = data['userData']['comment']
        
        # Обновляем статус заказа
        cart.status = OrderStatus.PROCESSING
        cart.is_ordered = True
        cart.updated_at = datetime.now()
        
        await session.commit()
        
        return {"success": True, "orderId": cart.id}
        
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.middleware("http")
async def log_requests(request, call_next):
    print(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    print(f"Response: {response.status_code}")
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7770)

