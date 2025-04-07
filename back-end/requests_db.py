from sqlalchemy import select, update, delete, func , and_ , desc, or_
from models import async_session, User, Categori, Products, ProductImage , Cart , CartItem , Reaction , ProductVariants , SortOrder, ProductFilter, ConciergeRequest
from pydantic import BaseModel, ConfigDict
from typing import List
import secrets
from datetime import datetime, timedelta
import json

LIMIT = 90

class CategorisShema(BaseModel):
    id:int
    name:str
    parent_id:int
    model_config = ConfigDict(from_attributes=True)

class ProductsShema(BaseModel):
    id:int
    name:str
    description:str
    price:float
    old_price:float
    categori:int

    model_config = ConfigDict(from_attributes=True)


class ProductsImagesShema(BaseModel):
    id:int
    product_id:int
    image_url:str
    is_main:bool

    model_config = ConfigDict(from_attributes=True)



async def get_or_create_user(tg_id:int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            return  {
                "id": user.id,
                "is_admin": user.is_admin,
                "auth_token": user.auth_token
            }
        else:
            auth_token = secrets.token_hex(16)
            user = User(tg_id= tg_id, is_admin=False, name='', phone='', email='', address='', comment='', auth_token=auth_token)
            session.add(user)
            await session.commit()
            await session.refresh(user)
        return {
            "id": user.id,
            "is_admin": user.is_admin,
            #"auth_token": user.auth_token
        }
  



async def get_categoris():
    async with async_session() as session:
        # Получаем все категории
        categories = await session.scalars(
            select(Categori)
            .where(Categori.parent_id == None)  # Получаем только основные категории
        )
        
        result = []
        for category in categories:
            # Получаем подкатегории для каждой основной категории
            subcategories = await session.scalars(
                select(Categori)
                .where(Categori.parent_id == category.id)
            )
            
            # Формируем структуру категории
            category_data = {
                "id": category.id,
                "name": category.name,
                "image": category.image_url,
                "subcategories": [
                    {
                        "id": sub.id,
                        "name": sub.name,
                        "image": sub.image_url
                    } for sub in subcategories 
                ] if subcategories else []
            }
            result.append(category_data)
        print(result)
        return result
    

async def get_product_by_id(product_id: int, user_id: int = None):
    async with async_session() as session:
        # Получаем основные данные о продукте
        product = await session.scalar(select(Products).where(Products.id == product_id))
        if not product:
            return None

        # Получаем категорию
        category = await session.scalar(select(Categori).where(Categori.id == product.categori_id))
        
        # Получаем изображения
        images = await session.scalars(
            select(ProductImage)
            .where(ProductImage.product_id == product.id)
        )
        
        # Получаем варианты
        variants = await session.scalars(
            select(ProductVariants)
            .where(ProductVariants.product_id == product.id)
        )
        
        # Проверяем лайк и корзину если есть user_id
        is_liked = False
        is_in_cart = False
        if user_id:
            # Проверяем лайк
            like = await session.scalar(
                select(Reaction)
                .where(
                    Reaction.user_id == user_id,
                    Reaction.product_id == product_id
                )
            )
            is_liked = bool(like)

            # Проверяем корзину
            cart = await session.scalar(
                select(Cart)
                .where(
                    Cart.user_id == user_id,
                    Cart.is_ordered == False
                )
            )
            if cart:
                cart_item = await session.scalar(
                    select(CartItem)
                    .where(
                        CartItem.cart_id == cart.id,
                        CartItem.product_id == product_id
                    )
                )
                is_in_cart = bool(cart_item)

        # Получаем похожие продукты
        related = await session.scalars(
            select(Products)
            .where(
                Products.categori_id == product.categori_id,
                Products.id != product.id,
                Products.visibility == True
            )
            .limit(3)
        )

        # Формируем список похожих продуктов
        related_products = []
        for rel in related:
            main_image = await session.scalar(
                select(ProductImage)
                .where(
                    ProductImage.product_id == rel.id,
                    ProductImage.is_main == True
                )
            )
            if not main_image:
                main_image = await session.scalar(
                    select(ProductImage)
                    .where(ProductImage.product_id == rel.id)
                )
            
            related_products.append({
                "id": rel.id,
                "name": rel.name,
                "productPrice": float(rel.price),
                "productOldPrice": float(rel.old_price),
                "image": main_image.image_url if main_image else None
            })

        return {
            "productId": product.id,
            "productName": product.name,
            "productDescription": product.description,
            "productPrice": float(product.price),
            "productOldPrice": float(product.old_price),
            "productCategory": category.name if category else None,
            "productBrand": product.brend,
            "productImages": [{"image_url": img.image_url} for img in images],
            "productsVariants": [
                {"variant_id": var.id, "variant_name": var.name}
                for var in variants
            ],
            "isLiked": is_liked,
            "isInCart": is_in_cart,
            "selectedVariant": None,
            "swiperOptions": {
                "pagination": {
                    "el": '.swiper-pagination'
                }
            },
            "defaultVariantText": 'Выберите размер',
            "relatedProducts": related_products
        }



async def get_products_data(parent_id: int, user_id: int, page: int, limit: int):
    offset = (page - 1) * limit
    async with async_session() as session:
        # Получаем категории
        categories = await session.scalars(select(Categori).where(Categori.visibility == True, 
                                                                  Categori.parent_id == parent_id))
        category_ids = [cat.id for cat in categories]
        serialized_categories = [
            {
                "id": cat.id,
                "name": cat.name,
                "image_url": cat.image
            } for cat in categories
        ]

        # Получаем продукты
        products = await session.scalars(select(Products).where(
            Products.visibility == True,
            Products.categori.in_(category_ids)).order_by(Products.created_at.desc()).offset(offset).limit(limit))
        # Получаем реакции пользователя
        user_reactions = await session.scalars(select(Reaction).where(Reaction.user_id == user_id))
        liked_product_ids = {reaction.product_id for reaction in user_reactions}

        serialized_products = [
            {
                "id": prod.id,
                "name": prod.name,
                "price": prod.price,
                "old_price": prod.old_price,
                "product_images": (await session.scalars(select(ProductImage).where(ProductImage.product_id == prod.id))).first().image_url if await session.scalars(select(ProductImage).where(ProductImage.product_id == prod.id)) else None,
                "is_liked": prod.id in liked_product_ids
            } for prod in products
        ]

        return {
            "page": page,
            "limit": limit,
            "categories": serialized_categories,
            "product_list": serialized_products
        }


async def get_dashboard_data(user_id: int, page: int, limit: int):
    offset = (page - 1) * limit
    async with async_session() as session:
        # Получаем категории
        categories = await session.scalars(select(Categori).where(Categori.visibility == True, 
                                                                  Categori.parent_id == None))
        serialized_categories = [
            {
                "id": cat.id,
                "name": cat.name,
                "image_url": cat.image
            } for cat in categories
        ]

        # Получаем продукты
        products = await session.scalars(select(Products).where(
            Products.visibility == True).order_by(Products.created_at.desc()).offset(offset).limit(limit))
        # Получаем реакции пользователя
        user_reactions = await session.scalars(select(Reaction).where(Reaction.user_id == user_id))
        liked_product_ids = {reaction.product_id for reaction in user_reactions}

        serialized_products = [
            {
                "id": prod.id,
                "name": prod.name,
                "price": prod.price,
                "old_price": prod.old_price,
                "product_images": (await session.scalars(select(ProductImage).where(ProductImage.product_id == prod.id))).first().image_url if await session.scalars(select(ProductImage).where(ProductImage.product_id == prod.id)) else None,
                "is_liked": prod.id in liked_product_ids
            } for prod in products
        ]

        return {
            "page": page,
            "limit": limit,
            "categories": serialized_categories,
            "product_list": serialized_products
        }


async def get_product_admin(product_id: int, user_id: int):
    async with async_session() as session:
        # Проверяем, является ли пользователь администратором
        user = await session.scalar(select(User).where(User.id == user_id))
        if not user or not user.is_admin:
            return {"error": "Доступ запрещен, пользователь не является администратором."}
        
        # Получаем продукт
        product = await session.scalar(select(Products).where(Products.id == product_id))
        if not product:
            return {"error": "Продукт не найден."}
        
        # Получаем варианты продукта
        variants = await session.scalars(select(ProductVariants).where(ProductVariants.product_id == product.id))
        
        category_list_all = await session.scalars(select(Categori))
        # Получаем изображения продукта
        category_list_all = [
            {"id": cat.id, "name": f"{cat.name}/{cat.parent.name}" if cat.parent else cat.name}
            for cat in category_list_all
        ]
        # Получаем изображения продукта
        images = await session.scalars(select(ProductImage).where(ProductImage.product_id == product.id))
        
        category_list_all = [
            {"id": cat.id, "name": f"{cat.name}/{cat.parent.name}" if cat.parent else cat.name}
            for cat in category_list_all
        ]
        
        return {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "old_price": product.old_price,
            "categori": product.categori.name,  
            "brend": product.brend,        
            "variants": [{"id": variant.id, "name": variant.name} for variant in variants],
            "images": [{"id": img.id, "image_url": img.image_url} for img in images],
            "category_list_all": category_list_all
        }

async def get_category_list_admin(user_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        if not user or not user.is_admin:
            return {"error": "Доступ запрещен, пользователь не является администратором."}
        
        category_list_all = await session.scalars(select(Categori))
        return [{"id": cat.id, "name": f"{cat.name}/{cat.parent.name}" if cat.parent else cat.name} for cat in category_list_all]


async def get_products_list_admin(user_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        if not user or not user.is_admin:
            return {"error": "Доступ запрещен, пользователь не является администратором."}
        
        products = await session.scalars(select(Products))
        return [{"id": prod.id, "name": prod.name , 
                 "price": prod.price, "visibility": prod.visibility} for prod in products]
    

async def get_reactions_list(user_id: int):
    async with async_session() as session:
        
        # Получаем реакции пользователя
        reactions =await session.scalars(select(Reaction).where(Reaction.user_id == user_id))
        liked_product_ids = {reaction.product_id for reaction in reactions}
        # Получаем продукты
        products = await session.scalars(select(Products).where(
            Products.visibility == True,
            Products.id.in_(liked_product_ids)
            ).order_by(Products.created_at.desc()))
        # Получаем реакции пользователя
        serialized_products = [
            {
                "id": prod.id,
                "name": prod.name,
                "price": prod.price,
                "old_price": prod.old_price,
                "product_images": (await session.scalars(select(ProductImage).where(
                    ProductImage.product_id == prod.id))).first().image_url if await session.scalars(select(ProductImage).where(ProductImage.product_id == prod.id)) else None,
                "is_liked": prod.id in liked_product_ids
            } for prod in products
        ]

        return {
            "product_list": serialized_products
        }
    
async def put_reaction(user_id: int, product_id: int):
    async with async_session() as session:
        reaction = await session.scalar(select(Reaction).where(Reaction.user_id == user_id, Reaction.product_id == product_id))
        if reaction:
            await session.delete(reaction)
        else:
            reaction = Reaction(user_id=user_id, product_id=product_id)
            session.add(reaction)
        await session.commit()

        return {"success": "200"}
    

async def get_cart_list(user_id: int):
    async with async_session() as session:
        cart = await session.scalar(select(Cart).where(Cart.user_id == user_id , Cart.is_ordered == False))
        if not cart:
            cart = Cart(user_id=user_id, is_ordered=False)
            session.add(cart)
            await session.commit()
            await session.refresh(cart)
        
        cart_items = await session.scalars(select(CartItem).where(CartItem.cart_id == cart.id))
        return {
            "id": cart.id,
            "user_id": cart.user_id,
            "is_ordered": cart.is_ordered,
            "cart_items": [
                {
                    "id": item.id, 
                    "product_id": item.product_id, 
                    "quantity": item.quantity,
                    "variants_id": item.variants_id
                } for item in cart_items
            ]
        }
    
async def add_to_cart(user_id: int, product_id: int,  quantity: int , variants_id: int = None):
    async with async_session() as session:
        cart = await session.scalar(select(Cart).where(Cart.user_id == user_id, Cart.is_ordered == False))
        if not cart:
            cart = Cart(user_id=user_id, is_ordered=False)
            session.add(cart)
            await session.commit()
            await session.refresh(cart)
        
        cart_item = CartItem(cart_id=cart.id, product_id=product_id, variants_id=variants_id, quantity=quantity)
        session.add(cart_item)
        await session.commit()
        await session.refresh(cart_item)
        
        return {"success": "200"}
    
async def delete_from_cart(user_id: int, product_id: int):
    async with async_session() as session:
        cart = await session.scalar(select(Cart).where(Cart.user_id == user_id, Cart.is_ordered == False))
        if not cart:
            return {"error": "Корзина не найдена."}
        
        cart_item = await session.scalar(select(CartItem).where(CartItem.cart_id == cart.id, CartItem.product_id == product_id))
        await session.delete(cart_item)
        await session.commit()
        
        return {"success": "200"}
    
async def get_products_by_category(
    category_id: int, 
    limit: int = 30, 
    offset: int = 0, 
    filters: ProductFilter | None = None
):
    async with async_session() as session:
        # Базовый запрос
        query = select(Products).where(Products.categori == category_id)
        count_query = select(func.count(Products.id)).where(Products.categori == category_id)

        # Применяем фильтры
        if filters:
            if filters.brand:
                query = query.where(Products.brend == filters.brand)
                count_query = count_query.where(Products.brend == filters.brand)
            
            if filters.min_price is not None:
                query = query.where(Products.price >= filters.min_price)
                count_query = count_query.where(Products.price >= filters.min_price)
            
            if filters.max_price is not None:
                query = query.where(Products.price <= filters.max_price)
                count_query = count_query.where(Products.price <= filters.max_price)
            
            if filters.size:
                # Подзапрос для фильтрации по размеру
                size_subquery = select(ProductVariants.product_id)\
                    .where(ProductVariants.name == filters.size)
                query = query.where(Products.id.in_(size_subquery))
                count_query = count_query.where(Products.id.in_(size_subquery))
            
            # Сортировка по цене
            if filters.price_order:
                if filters.price_order == SortOrder.ASC:
                    query = query.order_by(Products.price.asc())
                else:
                    query = query.order_by(Products.price.desc())

        # Применяем пагинацию
        query = query.limit(limit).offset(offset)
        
        # Получаем общее количество с учетом фильтров
        total = await session.scalar(count_query)
        
        # Получаем отфильтрованные товары
        result = await session.execute(query)
        products = result.scalars().all()

        # Дополняем данными о картинках и статусах
        for product in products:
            images_query = select(ProductImage).where(ProductImage.product_id == product.id)
            product.images = (await session.execute(images_query)).scalars().all()
            product.is_liked = False
            product.is_in_cart = False

        return products, total
    

async def search_products(query: str, limit: int = 10):
    async with async_session() as session:
        # Поиск по имени продукта и бренду
        search_query = f"%{query}%"
        query = select(Products)\
            .where(
                or_(
                    Products.name.ilike(search_query),
                    Products.brend.ilike(search_query),
                    Products.description.ilike(search_query)
                )
            )\
            .limit(limit)
        
        result = await session.execute(query)
        products = result.scalars().all()

        # Загружаем изображения и категории для каждого продукта
        for product in products:
            # Загрузка изображений
            images_query = select(ProductImage).where(ProductImage.product_id == product.id)
            product.images = (await session.execute(images_query)).scalars().all()
            
            # Загрузка категории
            category_query = select(Categori).where(Categori.id == product.categori)
            category = await session.scalar(category_query)
            product.category_name = category.name if category else None

        return products
    

async def get_dashboard_stats():
    async with async_session() as session:
        # Получаем количество новых заказов за неделю
        week_ago = datetime.now() - timedelta(days=7)
        new_orders = await session.scalar(
            select(func.count(Cart.id))
            .where(Cart.created_at >= week_ago)
        )
        
        # Общее количество товаров
        total_products = await session.scalar(
            select(func.count(Products.id))
        )
        
        # Общее количество пользователей
        total_users = await session.scalar(
            select(func.count(User.id))
        )
        
        # Активные заказы
        active_orders = await session.scalar(
            select(func.count(Cart.id))
            .where(Cart.is_ordered == True)
            .where(Cart.status != 'completed')
        )
        
        return {
            "newOrders": new_orders,
            "totalProducts": total_products,
            "totalUsers": total_users,
            "activeOrders": active_orders
        }

async def get_popular_products(limit: int = 10):
    async with async_session() as session:
        # Подзапрос для подсчета реакций
        reactions_subquery = (
            select(
                Reaction.product_id,
                func.count(Reaction.id).label('reaction_count')
            )
            .group_by(Reaction.product_id)
            .subquery()
        )
        
        # Получаем популярные товары
        query = (
            select(
                Products,
                func.coalesce(reactions_subquery.c.reaction_count, 0)
            )
            .outerjoin(
                reactions_subquery,
                Products.id == reactions_subquery.c.product_id
            )
            .order_by(reactions_subquery.c.reaction_count.desc())
            .limit(limit)
        )
        
        result = await session.execute(query)
        products = []
        
        for product, reactions_count in result:
            # Получаем основное изображение товара
            image_query = select(ProductImage).where(
                ProductImage.product_id == product.id,
                ProductImage.is_main == True
            )
            image = await session.scalar(image_query)
            
            products.append({
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "reactions": reactions_count,
                "image": image.image_url if image else None
            })
        
        return products
    

async def create_or_update_product(
    product_id: int = None,
    name: str = None,
    description: str = None,
    price: float = None,
    old_price: float = None,
    visibility: bool = True,
    category: int = None,
    brand: str = None,
    product_type: str = None,
    variants: list = None,
    images: list = None
):
    async with async_session() as session:
        if product_id:
            # Обновление существующего продукта
            product = await session.get(Products, product_id)
            if not product:
                raise ValueError("Продукт не найден")
        else:
            # Создание нового продукта
            product = Products()
        
        # Обновляем данные продукта
        product.name = name
        product.description = description
        product.price = price
        product.old_price = old_price
        product.visibility = visibility
        product.categori = category
        product.brend = brand
        
        if not product_id:
            session.add(product)
        
        await session.commit()
        await session.refresh(product)
        
        # Обновляем варианты
        if variants:
            # Удаляем старые варианты
            await session.execute(
                delete(ProductVariants).where(ProductVariants.product_id == product.id)
            )
            
            # Добавляем новые варианты
            for variant in variants:
                new_variant = ProductVariants(
                    product_id=product.id,
                    name=variant['variant_name']
                )
                session.add(new_variant)
        
        # Обновляем изображения
        if images:
            # Удаляем старые изображения
            await session.execute(
                delete(ProductImage).where(ProductImage.product_id == product.id)
            )
            
            # Добавляем новые изображения
            for image_url in images:
                new_image = ProductImage(
                    product_id=product.id,
                    image_url=image_url,
                    is_main=False  # Можно добавить логику определения главного изображения
                )
                session.add(new_image)
        
        await session.commit()
        return product
    

async def get_categories_tree():
    async with async_session() as session:
        # Получаем все категории
        categories = await session.scalars(select(Categori))
        
        # Создаем словарь для быстрого доступа к категориям
        categories_dict = {}
        for category in categories:
            categories_dict[category.id] = {
                "id": category.id,
                "name": category.name,
                "image": category.image_url,
                "parent_id": category.parent_id,
                "children": []
            }
        
        # Строим дерево
        root_categories = []
        for category_id, category_data in categories_dict.items():
            if category_data["parent_id"] is None:
                root_categories.append(category_data)
            else:
                parent = categories_dict.get(category_data["parent_id"])
                if parent:
                    parent["children"].append(category_data)
        
        return root_categories

async def create_category(name: str, parent_id: int = None, image_url: str = None):
    async with async_session() as session:
        category = Categori(
            name=name,
            parent_id=parent_id,
            image_url=image_url,
            visibility=True
        )
        session.add(category)
        await session.commit()
        await session.refresh(category)
        
        return {
            "id": category.id,
            "name": category.name,
            "image": category.image_url,
            "parent_id": category.parent_id
        }

async def update_category(category_id: int, name: str, parent_id: int = None, image_url: str = None):
    async with async_session() as session:
        category = await session.scalar(
            select(Categori).where(Categori.id == category_id)
        )
        
        if not category:
            raise ValueError("Category not found")
        
        # Обновляем только если значение передано
        if name:
            category.name = name
        if parent_id is not None:
            category.parent_id = parent_id
        if image_url:
            category.image_url = image_url
            
        await session.commit()
        await session.refresh(category)
        
        return {
            "id": category.id,
            "name": category.name,
            "image": category.image_url,
            "parent_id": category.parent_id
        }

async def delete_category(category_id: int):
    async with async_session() as session:
        # Проверяем есть ли подкатегории
        subcategories = await session.scalar(
            select(Categori).where(Categori.parent_id == category_id)
        )
        
        if subcategories:
            raise ValueError("Cannot delete category with subcategories")
        
        # Проверяем есть ли товары
        products = await session.scalar(
            select(Products).where(Products.categori_id == category_id)
        )
        
        if products:
            raise ValueError("Cannot delete category with products")
        
        # Удаляем категорию
        await session.execute(
            delete(Categori).where(Categori.id == category_id)
        )
        await session.commit()

async def get_best_products(limit: int = 30):
    async with async_session() as session:
        # Получаем продукты с изображениями
        products = await session.scalars(
            select(Products)
            .where(Products.visibility == True)
            .order_by(desc(Products.created_at))
            .limit(limit)
        )
        
        result = []
        for product in products:
            # Получаем главное изображение продукта
            main_image = await session.scalar(
                select(ProductImage)
                .where(
                    ProductImage.product_id == product.id,
                    ProductImage.is_main == True
                )
            )
            
            # Если нет главного изображения, берем первое
            if not main_image:
                main_image = await session.scalar(
                    select(ProductImage)
                    .where(ProductImage.product_id == product.id)
                )
            
            product_data = {
                "id": product.id,
                "name": product.name,
                "productPrice": float(product.price),
                "productOldPrice": float(product.old_price),
                "image": main_image.image_url if main_image else None,
                "like": False  # По умолчанию не в избранном
            }
            result.append(product_data)
            
        return result

async def get_cart_items(user_id: int):
    async with async_session() as session:
        # Получаем активную корзину пользователя
        cart = await session.scalar(
            select(Cart)
            .where(
                Cart.user_id == user_id,
                Cart.is_ordered == False
            )
        )
        
        if not cart:
            return []
            
        # Получаем товары в корзине
        cart_items = await session.scalars(
            select(CartItem)
            .where(CartItem.cart_id == cart.id)
        )
        
        result = []
        for cart_item in cart_items:
            # Получаем информацию о продукте
            product = await session.scalar(
                select(Products)
                .where(Products.id == cart_item.product_id)
            )
            
            if not product:
                continue
                
            # Получаем главное изображение продукта
            main_image = await session.scalar(
                select(ProductImage)
                .where(
                    ProductImage.product_id == product.id,
                    ProductImage.is_main == True
                )
            )
            
            if not main_image:
                main_image = await session.scalar(
                    select(ProductImage)
                    .where(ProductImage.product_id == product.id)
                )
            
            # Получаем вариант если есть
            variant = None
            if cart_item.variants_id:
                variant = await session.scalar(
                    select(ProductVariants)
                    .where(ProductVariants.id == cart_item.variants_id)
                )
            
            item_data = {
                "id": cart_item.id,
                "name": product.name,
                "productPrice": float(product.price),
                "productOldPrice": float(product.old_price),
                "productDescription": product.description,
                "image_url": main_image.image_url if main_image else None,
                "variant": variant.name if variant else None,
                "removing": False
            }
            result.append(item_data)
            
        return result

async def get_order_history(user_id: int):
    async with async_session() as session:
        # Получаем все заказы пользователя (завершенные корзины)
        orders = await session.scalars(
            select(Cart)
            .where(
                Cart.user_id == user_id,
                Cart.is_ordered == True
            )
            .order_by(desc(Cart.created_at))
        )
        
        result = []
        for order in orders:
            # Получаем товары заказа
            cart_items = await session.scalars(
                select(CartItem)
                .where(CartItem.cart_id == order.id)
            )
            
            items = []
            total_price = 0
            
            for cart_item in cart_items:
                product = await session.scalar(
                    select(Products)
                    .where(Products.id == cart_item.product_id)
                )
                
                if not product:
                    continue
                    
                # Получаем изображение товара
                main_image = await session.scalar(
                    select(ProductImage)
                    .where(
                        ProductImage.product_id == product.id,
                        ProductImage.is_main == True
                    )
                )
                
                if not main_image:
                    main_image = await session.scalar(
                        select(ProductImage)
                        .where(ProductImage.product_id == product.id)
                    )
                
                # Получаем вариант если есть
                variant = None
                if cart_item.variants_id:
                    variant = await session.scalar(
                        select(ProductVariants)
                        .where(ProductVariants.id == cart_item.variants_id)
                    )
                
                item_data = {
                    "id": cart_item.id,
                    "name": product.name,
                    "price": float(product.price),
                    "description": product.description,
                    "image_url": main_image.image_url if main_image else None,
                    "variant": variant.name if variant else None
                }
                items.append(item_data)
                total_price += float(product.price)
            
            order_data = {
                "order_id": order.id,
                "created_at": order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "status": order.status,
                "total_price": total_price,
                "items": items
            }
            result.append(order_data)
            
        return result

async def get_favorite_products(user_id: int):
    async with async_session() as session:
        # Получаем все лайки пользователя
        reactions = await session.scalars(
            select(Reaction)
            .where(Reaction.user_id == user_id)
        )
        
        result = []
        for reaction in reactions:
            # Получаем информацию о продукте
            product = await session.scalar(
                select(Products)
                .where(
                    Products.id == reaction.product_id,
                    Products.visibility == True
                )
            )
            
            if not product:
                continue
                
            # Получаем главное изображение продукта
            main_image = await session.scalar(
                select(ProductImage)
                .where(
                    ProductImage.product_id == product.id,
                    ProductImage.is_main == True
                )
            )
            
            if not main_image:
                main_image = await session.scalar(
                    select(ProductImage)
                    .where(ProductImage.product_id == product.id)
                )
            
            product_data = {
                "id": product.id,
                "name": product.name,
                "productPrice": float(product.price),
                "productOldPrice": float(product.old_price),
                "image": main_image.image_url if main_image else None,
                "like": True
            }
            result.append(product_data)
            
        return result

async def get_category_data(category_id: int, user_id: int = None):
    async with async_session() as session:
        # Получаем информацию о категории
        category = await session.scalar(
            select(Categori)
            .where(Categori.id == category_id)
        )
        
        if not category:
            return None
            
        # Получаем подкатегории
        subcategories = await session.scalars(
            select(Categori)
            .where(Categori.parent_id == category_id)
        )
        
        # Получаем товары текущей категории
        products = await session.scalars(
            select(Products)
            .where(
                Products.categori_id == category_id,
                Products.visibility == True
            )
            .order_by(desc(Products.created_at))
        )
        
        # Формируем список подкатегорий
        subcategories_data = []
        for sub in subcategories:
            subcategories_data.append({
                "id": sub.id,
                "name": sub.name,
                "image": sub.image_url
            })
            
        # Формируем список товаров
        products_data = []
        for product in products:
            # Получаем главное изображение
            main_image = await session.scalar(
                select(ProductImage)
                .where(
                    ProductImage.product_id == product.id,
                    ProductImage.is_main == True
                )
            )
            
            if not main_image:
                main_image = await session.scalar(
                    select(ProductImage)
                    .where(ProductImage.product_id == product.id)
                )
                
            # Проверяем лайк если есть user_id
            is_liked = False
            if user_id:
                like = await session.scalar(
                    select(Reaction)
                    .where(
                        Reaction.user_id == user_id,
                        Reaction.product_id == product.id
                    )
                )
                is_liked = bool(like)
            
            product_data = {
                "id": product.id,
                "name": product.name,
                "productPrice": float(product.price),
                "productOldPrice": float(product.old_price),
                "image": main_image.image_url if main_image else None,
                "like": is_liked
            }
            products_data.append(product_data)
            
        return {
            "category": {
                "id": category.id,
                "name": category.name,
                "image": category.image_url
            },
            "subcategories": subcategories_data,
            "products": products_data
        }

async def create_product(
    name: str,
    description: str,
    price: float,
    old_price: float,
    category_id: int,
    brand: str = None,
    variants: str = None,
    images: list = None,
    main_image_index: int = 0
):
    async with async_session() as session:
        # Создаем продукт
        product = Products(
            name=name,
            description=description,
            price=price,
            old_price=old_price,
            categori_id=category_id,
            brend=brand,
            visibility=True
        )
        session.add(product)
        await session.commit()
        await session.refresh(product)
        
        # Добавляем изображения
        if images:
            for i, image_url in enumerate(images):
                image = ProductImage(
                    product_id=product.id,
                    image_url=image_url,
                    is_main=(i == main_image_index)
                )
                session.add(image)
        
        # Добавляем варианты
        if variants:
            variants_data = json.loads(variants)
            for variant_data in variants_data:
                variant = ProductVariants(
                    product_id=product.id,
                    name=variant_data['name']
                )
                session.add(variant)
        
        await session.commit()
        
        return {
            "id": product.id,
            "name": product.name,
            "price": float(product.price),
            "category_id": product.categori_id
        }

async def update_product(
    product_id: int,
    name: str = None,
    description: str = None,
    price: float = None,
    old_price: float = None,
    category_id: int = None,
    brand: str = None,
    variants: str = None,
    new_images: list = None,
    main_image_index: int = None,
    deleted_images: str = None
):
    async with async_session() as session:
        product = await session.scalar( 
            select(Products).where(Products.id == product_id)
        )
        
        if not product:
            raise ValueError("Product not found")
        
        # Обновляем основные данные
        if name:
            product.name = name
        if description:
            product.description = description
        if price is not None:
            product.price = price
        if old_price is not None:
            product.old_price = old_price
        if category_id:
            product.categori_id = category_id
        if brand:
            product.brend = brand
            
        # Удаляем выбранные изображения
        if deleted_images:
            deleted_ids = json.loads(deleted_images)
            await session.execute(
                delete(ProductImage)
                .where(ProductImage.id.in_(deleted_ids))
            )
            
        # Добавляем новые изображения
        if new_images:
            current_images = await session.scalars(
                select(ProductImage)
                .where(ProductImage.product_id == product_id)
            )
            current_count = len(list(current_images))
            
            for i, image_url in enumerate(new_images):
                image = ProductImage(
                    product_id=product_id,
                    image_url=image_url,
                    is_main=(current_count + i == main_image_index if main_image_index is not None else False)
                )
                session.add(image)
                
        # Обновляем варианты
        if variants:
            # Удаляем старые варианты
            await session.execute(
                delete(ProductVariants)
                .where(ProductVariants.product_id == product_id)
            )
            
            # Добавляем новые
            variants_data = json.loads(variants)
            for variant_data in variants_data:
                variant = ProductVariants(
                    product_id=product_id,
                    name=variant_data['name']
                )
                session.add(variant)
        
        await session.commit()
        await session.refresh(product)
        
        return {
            "id": product.id,
            "name": product.name,
            "price": float(product.price),
            "category_id": product.categori_id
        }

async def delete_product(product_id: int):
    async with async_session() as session:
        # Удаляем связанные данные
        await session.execute(
            delete(ProductImage)
            .where(ProductImage.product_id == product_id)
        )
        
        await session.execute(
            delete(ProductVariants)
            .where(ProductVariants.product_id == product_id)
        )
        
        # Удаляем сам продукт
        await session.execute(
            delete(Products)
            .where(Products.id == product_id)
        )
        
        await session.commit()

async def get_admin_products(
    page: int = 1,
    limit: int = 20,
    category_id: int = None,
    search: str = None
):
    async with async_session() as session:
        query = select(Products)
        
        # Применяем фильтры
        if category_id:
            query = query.where(Products.categori_id == category_id)
            
        if search:
            query = query.where(
                or_(
                    Products.name.ilike(f"%{search}%"),
                    Products.description.ilike(f"%{search}%")
                )
            )
        
        # Добавляем пагинацию
        total = await session.scalar(
            select(func.count()).select_from(query.subquery())
        )
        
        products = await session.scalars(
            query
            .order_by(desc(Products.created_at))
            .offset((page - 1) * limit)
            .limit(limit)
        )
        
        result = []
        for product in products:
            # Получаем главное изображение
            main_image = await session.scalar(
                select(ProductImage)
                .where(
                    ProductImage.product_id == product.id,
                    ProductImage.is_main == True
                )
            )
            
            if not main_image:
                main_image = await session.scalar(
                    select(ProductImage)
                    .where(ProductImage.product_id == product.id)
                )
            
            # Получаем категорию
            category = await session.scalar(
                select(Categori)
                .where(Categori.id == product.categori_id)
            )
            
            result.append({
                "id": product.id,
                "name": product.name,
                "price": float(product.price),
                "old_price": float(product.old_price),
                "category": category.name if category else None,
                "brand": product.brend,
                "image": main_image.image_url if main_image else None,
                "visibility": product.visibility
            })
            
        return {
            "items": result,
            "total": total,
            "pages": (total + limit - 1) // limit
        }

async def get_admin_statistics():
    async with async_session() as session:
        # Общее количество товаров
        total_products = await session.scalar(
            select(func.count()).select_from(Products)
        )
        
        # Количество активных товаров
        active_products = await session.scalar(
            select(func.count())
            .select_from(Products)
            .where(Products.visibility == True)
        )
        
        # Количество категорий
        total_categories = await session.scalar(
            select(func.count()).select_from(Categori)
        )
        
        # Количество заказов
        total_orders = await session.scalar(
            select(func.count())
            .select_from(Cart)
            .where(Cart.is_ordered == True)
        )
        
        # Количество заказов за последние 30 дней
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_orders = await session.scalar(
            select(func.count())
            .select_from(Cart)
            .where(
                Cart.is_ordered == True,
                Cart.created_at >= thirty_days_ago)
        )
        
        # Общая сумма заказов
        total_revenue = await session.scalar(
            select(func.sum(Products.price))
            .select_from(Cart)
            .join(CartItem, CartItem.cart_id == Cart.id)
            .join(Products, Products.id == CartItem.product_id)
            .where(Cart.is_ordered == True)
        )
        
        # Сумма заказов за последние 30 дней
        recent_revenue = await session.scalar(
            select(func.sum(Products.price))
            .select_from(Cart)
            .join(CartItem, CartItem.cart_id == Cart.id)
            .join(Products, Products.id == CartItem.product_id)
            .where(
                Cart.is_ordered == True,
                Cart.created_at >= thirty_days_ago)
        )
        
        # Популярные категории
        popular_categories = await session.execute(
            select(
                Categori.name,
                func.count(Products.id).label('product_count')
            )
            .join(Products, Products.categori_id == Categori.id)
            .group_by(Categori.id)
            .order_by(desc('product_count'))
            .limit(5)
        )
        
        popular_categories_list = [
            {"name": row[0], "count": row[1]}
            for row in popular_categories
        ]
        
        return {
            "products": {
                "total": total_products,
                "active": active_products
            },
            "categories": {
                "total": total_categories,
                "popular": popular_categories_list
            },
            "orders": {
                "total": total_orders,
                "recent": recent_orders
            },
            "revenue": {
                "total": float(total_revenue) if total_revenue else 0,
                "recent": float(recent_revenue) if recent_revenue else 0
            }
        }

async def get_admin_orders(page: int = 1, limit: int = 20, status: str = None):
    async with async_session() as session:
        query = select(Cart).where(Cart.is_ordered == True)
        
        if status:
            query = query.where(Cart.status == status)
            
        # Добавляем пагинацию
        total = await session.scalar(
            select(func.count()).select_from(query.subquery())
        )
        
        orders = await session.scalars(
            query
            .order_by(desc(Cart.created_at))
            .offset((page - 1) * limit)
            .limit(limit)
        )
        
        result = []
        for order in orders:
            # Получаем пользователя
            user = await session.scalar(
                select(User).where(User.id == order.user_id)
            )
            
            # Получаем товары заказа
            cart_items = await session.scalars(
                select(CartItem)
                .where(CartItem.cart_id == order.id)
            )
            
            items = []
            total_price = 0
            
            for cart_item in cart_items:
                product = await session.scalar(
                    select(Products)
                    .where(Products.id == cart_item.product_id)
                )
                
                if not product:
                    continue
                    
                variant = None
                if cart_item.variants_id:
                    variant = await session.scalar(
                        select(ProductVariants)
                        .where(ProductVariants.id == cart_item.variants_id)
                    )
                
                items.append({
                    "name": product.name,
                    "price": float(product.price),
                    "variant": variant.name if variant else None
                })
                total_price += float(product.price)
            
            result.append({
                "id": order.id,
                "created_at": order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "status": order.status,
                "total_price": total_price,
                "items_count": len(items),
                "user": {
                    "id": user.id,
                    "tg_id": user.tg_id,
                    "name": user.name,
                    "phone": user.phone,
                    "email": user.email,
                    "address": user.address
                },
                "items": items
            })
            
        return {
            "items": result,
            "total": total,
            "pages": (total + limit - 1) // limit
        }

async def get_admin_products_list(page: int = 1, limit: int = 20, search: str = None, category_id: int = None):
    async with async_session() as session:
        query = select(Products)
        
        if search:
            query = query.where(Products.name.ilike(f"%{search}%"))
            
        if category_id:
            query = query.where(Products.categori_id == category_id)
            
        # Получаем общее количество
        total = await session.scalar(
            select(func.count()).select_from(query.subquery())
        )
        
        # Получаем товары с пагинацией
        products = await session.scalars(
            query
            .order_by(desc(Products.created_at))
            .offset((page - 1) * limit)
            .limit(limit)
        )
        
        result = []
        for product in products:
            # Получаем категорию
            category = await session.scalar(
                select(Categori).where(Categori.id == product.categori_id)
            )
            
            # Получаем главное изображение
            main_image = await session.scalar(
                select(ProductImage)
                .where(
                    ProductImage.product_id == product.id,
                    ProductImage.is_main == True
                )
            )
            
            if not main_image:
                main_image = await session.scalar(
                    select(ProductImage)
                    .where(ProductImage.product_id == product.id)
                )
            
            result.append({
                "id": product.id,
                "name": product.name,
                "price": float(product.price),
                "old_price": float(product.old_price),
                "category": category.name if category else None,
                "image": main_image.image_url if main_image else None,
                "visibility": product.visibility,
                "created_at": product.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })
            
        return {
            "items": result,
            "total": total,
            "pages": (total + limit - 1) // limit
        }

async def toggle_product_visibility(product_id: int):
    async with async_session() as session:
        product = await session.scalar(
            select(Products).where(Products.id == product_id)
        )
        
        if not product:
            raise ValueError("Product not found")
            
        product.visibility = not product.visibility
        await session.commit()
        
        return {"success": True, "visibility": product.visibility}

async def create_concierge_request(name: str, contact: str, product_link: str | None, details: str, user_id: int | None = None):
    async with async_session() as session:
        # Создаем новый запрос
        concierge_request = ConciergeRequest(
            name=name,
            contact=contact,
            product_link=product_link,
            details=details,
            user_id=user_id,
            status='new'
        )
        
        session.add(concierge_request)
        await session.commit()
        await session.refresh(concierge_request)
        
        return {
            "success": True,
            "message": "Ваш запрос успешно отправлен! Наш менеджер свяжется с вами в ближайшее время.",
            "request": {
                "id": concierge_request.id,
                "name": concierge_request.name,
                "contact": concierge_request.contact,
                "product_link": concierge_request.product_link,
                "details": concierge_request.details,
                "status": concierge_request.status,
                "created_at": concierge_request.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
        }

# Добавим также метод для получения списка запросов (для админ-панели)
async def get_concierge_requests(page: int = 1, limit: int = 20, status: str = None):
    async with async_session() as session:
        query = select(ConciergeRequest)
        
        if status:
            query = query.where(ConciergeRequest.status == status)
            
        # Получаем общее количество
        total = await session.scalar(
            select(func.count()).select_from(query.subquery())
        )
        
        # Получаем запросы с пагинацией
        requests = await session.scalars(
            query
            .order_by(desc(ConciergeRequest.created_at))
            .offset((page - 1) * limit)
            .limit(limit)
        )
        
        result = []
        for request in requests:
            # Получаем пользователя если есть
            user = None
            if request.user_id:
                user = await session.scalar(
                    select(User).where(User.id == request.user_id)
                )
            
            result.append({
                "id": request.id,
                "name": request.name,
                "contact": request.contact,
                "product_link": request.product_link,
                "details": request.details,
                "status": request.status,
                "created_at": request.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "user": {
                    "id": user.id,
                    "tg_id": user.tg_id,
                    "name": user.name
                } if user else None
            })
            
        return {
            "items": result,
            "total": total,
            "pages": (total + limit - 1) // limit
        }

# Метод для обновления статуса запроса
async def update_concierge_request_status(request_id: int, status: str):
    async with async_session() as session:
        request = await session.scalar(
            select(ConciergeRequest).where(ConciergeRequest.id == request_id)
        )
        
        if not request:
            raise ValueError("Request not found")
            
        request.status = status
        await session.commit()
        
        return {
            "success": True,
            "status": status
        }

async def get_user_by_tg_id(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(
            select(User).where(User.tg_id == str(tg_id))
        )
        if user:
            return {
                "id": user.id,
                "is_admin": user.is_admin,
                "tg_id": user.tg_id
            }
        return None


