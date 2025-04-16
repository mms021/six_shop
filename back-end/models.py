from sqlalchemy import ForeignKey, String, BigInteger, func, text
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, relationship, backref
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
import asyncpg  
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from sqlalchemy.sql import select
import secrets ,  os
load_dotenv()

ADMINS = os.getenv('TG_ADMINS').split(',')

DELETE_DATABASE = True if os.getenv('DELETE_DATABASE') == 'True' else False


POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')



#postgre_url=f"postgresql+asyncpg://postgres:123456@)/{POSTGRES_DB}"






ADMINS = [ {"tg_id": i.split('|')[0], "name": i.split('|')[1]} for i in ADMINS]


postgre_url = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

engine = create_async_engine(url=postgre_url, echo=True )

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass 

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[str] = mapped_column(String(128))
    tg_username: Mapped[str] = mapped_column(String(128) , nullable=True)
    channel_id: Mapped[str] = mapped_column(String(128) , nullable=True) 
    is_admin: Mapped[bool] = mapped_column(default=False)
    name: Mapped[str] = mapped_column(String(128), nullable=True)
    phone: Mapped[str] = mapped_column(String(128), nullable=True)
    email: Mapped[str] = mapped_column(String(128), nullable=True)
    address: Mapped[str] = mapped_column(String(512), nullable=True)
    comment: Mapped[str] = mapped_column(String(128), nullable=True)
    auth_token: Mapped[str] = mapped_column(String(128), nullable=True)

    created_at: Mapped[str] = mapped_column(default=func.now())
    updated_at: Mapped[str] = mapped_column(default=func.now(), onupdate=func.now())


class Categori(Base):
    __tablename__ = 'categoris'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    parent_id: Mapped[int | None] = mapped_column(ForeignKey('categoris.id'), nullable=True)
    visibility: Mapped[bool] = mapped_column(default=True)
    image_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    
    # Отношение для получения подкатегорий
    subcategories = relationship("Categori", 
                               backref=backref('parent', remote_side=[id]),
                               cascade="all, delete-orphan")

class Products(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    brend: Mapped[str] = mapped_column(String(128), default='')
    description: Mapped[str] = mapped_column(String(256), default='')
    categori_id: Mapped[int] = mapped_column(ForeignKey('categoris.id', ondelete='CASCADE' ))
    price: Mapped[float] = mapped_column(default=0.0)
    old_price: Mapped[float] = mapped_column(default=0.0)
    visibility: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[str] = mapped_column(default=func.now())
    updated_at: Mapped[str] = mapped_column(default=func.now(), onupdate=func.now())  

class ProductVariants(Base):
    __tablename__ = 'product_variants'
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    name: Mapped[str] = mapped_column(String(128))
    
    

class ProductImage(Base):
    __tablename__ = 'product_images'
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))  
    image_url: Mapped[str] = mapped_column(String(256))  
    is_main: Mapped[bool] = mapped_column(default=False)


class OrderStatus(str, Enum):
    NEW = "new"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Cart(Base):
    __tablename__ = 'carts'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    status: Mapped[str] = mapped_column(String(128), default=OrderStatus.NEW)
    is_ordered: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())
    

class CartItem(Base):
    __tablename__ = 'cart_items'
    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey('carts.id'))  
    
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id')) 
    variants_id: Mapped[int] = mapped_column(ForeignKey('product_variants.id'))
    is_available: Mapped[bool] = mapped_column(default=True)


class Reaction(Base):
    __tablename__ = 'reactions'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))  
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id')) 


class ProductResponse(BaseModel):
    id: int
    name: str
    productPrice: float
    productOldPrice: float
    productImages: List[str]  # список URL изображений
    isLiked: bool = False
    isInCart: bool = False
    brend: str | None = None
    description: str | None = None

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    image: str | None = None

class ProductDetailResponse(BaseModel):
    productId: int
    productName: str
    productDescription: str
    productPrice: float
    productOldPrice: float
    productCategory: str
    productBrand: str
    productImages: List[dict]  # список словарей с id и url изображений
    productsVariants: List[dict]  # список вариантов продукта
    isLiked: bool
    isInCart: bool





class ProductListResponse(BaseModel):
    products: List[ProductResponse]
    total: int
    hasMore: bool

class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"

class ProductFilter(BaseModel):
    price_order: SortOrder | None = None
    size: str | None = None
    brand: str | None = None
    min_price: float | None = None
    max_price: float | None = None

class ConciergeRequest(Base):
    __tablename__ = 'concierge_requests'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    contact: Mapped[str] = mapped_column(String(128))
    product_link: Mapped[str] = mapped_column(String(512), nullable=True)
    details: Mapped[str] = mapped_column(String(1024))
    status: Mapped[str] = mapped_column(String(32), default='new')  # new, processing, completed, cancelled
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())
    user_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'), nullable=True)
    
    # Отношение с пользователем
    user = relationship("User", backref="concierge_requests")

async def create_database():
    conn = await asyncpg.connect(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )
    if DELETE_DATABASE:
        await conn.execute(f'DROP DATABASE IF EXISTS {POSTGRES_DB};')
    
    databases = await conn.fetch("SELECT datname FROM pg_database;")

    if POSTGRES_DB not in [db['datname'] for db in databases]:
        await conn.execute(f'''
            CREATE DATABASE {POSTGRES_DB}
            WITH OWNER = postgres
            ENCODING = 'UTF8'
            TEMPLATE = template0;
        ''')
    else:
        print(f"База данных {POSTGRES_DB} уже существует.")
    await conn.close()

async def init_db():
    try:
        # Проверяем существование базы данных
        async with engine.connect() as conn:
            print("База данных существует и подключение успешно")
    except Exception as e:
        print("База данных не существует, создаем...")
        await create_database()
        print("База данных создана")

    try:
        # Проверяем существование таблиц
        async with engine.connect() as conn:
            # Проверяем наличие хотя бы одной таблицы
            result = await conn.run_sync(lambda sync_conn: sync_conn.execute(
                text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
            ))
            tables = await result.fetchall()
            
            if not tables:
                print("Таблицы не найдены, создаем...")
                async with engine.begin() as con:
                    await con.run_sync(Base.metadata.create_all)
                print("Таблицы созданы")
            else:
                print("Таблицы уже существуют")

        # Проверяем наличие админов
        async with async_session() as session:
            admin_exists = await session.scalar(
                select(User).where(User.is_admin == True)
            )

            if not admin_exists:
                print("Админы не найдены, создаем...")
                # Список дефолтных админов
                for admin_data in ADMINS:
                    admin = User(
                        tg_id=admin_data["tg_id"],
                        is_admin=True,
                        name=admin_data["name"],
                        phone='',
                        email='',
                        address='',
                        comment='',
                        auth_token=secrets.token_hex(16)
                    )
                    session.add(admin)
                    print(f"Создан админ: {admin.name}")
                
                await session.commit()
                print("Админы созданы")
            else:
                print("Админы уже существуют")

    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")
        raise



