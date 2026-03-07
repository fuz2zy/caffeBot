import asyncpg

from config import DATABASE_URL


async def init_db(pool: asyncpg.Pool):
    """Инициализация базы данных - создание таблиц"""

    await pool.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id BIGINT PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    await pool.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            description TEXT,
            available BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    await pool.execute("""
        CREATE TABLE IF NOT EXISTS cart_items (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT NOT NULL,
            product_id INTEGER NOT NULL REFERENCES products(id),
            quantity INTEGER NOT NULL DEFAULT 1,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(telegram_id, product_id)
        )
    """)


#----------ПОЛЬЗОВАТЕЛЬ----------


async def add_user(pool: asyncpg.Pool, id: int, username: str, first_name: str, last_name: str):
    """Добавить польователя или обновить если уже добавлен"""

    await pool.execute("""
                       INSERT INTO users (id)
                       VALUES ($1)
                       ON CONFLICT (id) DO UPDATE
                       SET username = $2, first_name = $3, last_name = $4
""", id, username, first_name, last_name)


async def get_user(pool: asyncpg.Pool, telegram_id: int):
    """Получить пользователя по telegram_id"""

    return await pool.fetchrow(
        "SELECT * FROM users WHERE id = $1", telegram_id
    )


async def get_users(pool: asyncpg.Pool):
    """Получить пользоватей"""

    return await pool.fetch(
        "SELECT * FROM users "
    )


#----------ТОВАРЫ----------


async def add_product(pool: asyncpg.Pool, name: str, price: float, description: str = 'Описание товара отсутсвует'):
    """Добавить товар"""

    await pool.execute("""
                       INSERT INTO products (name, price, description)
                       VALUES ($1, $2, $3)
""", name, price, description)


async def delete_product(pool: asyncpg.Pool, product_id: int):
    """Удалить товар"""

    await pool.execute(
        "DELETE FROM products WHERE id = $1", product_id
    )


async def hide_product(pool: asyncpg.Pool, product_id: int):
    """Скрывает продукт по product_id (использовать вместо удаления)"""

    await pool.execute(
        "UPDATE products SET available = FALSE WHERE id = $1", product_id
    )


async def show_product(pool: asyncpg.Pool, product_id: int):
    """Показывает продукт по product_id"""

    await pool.execute(
        "UPDATE products SET available = TRUE WHERE id = $1", product_id
    )


async def get_product(pool: asyncpg.Pool, product_id: int):
    """Получить продукт по product_id"""

    return await pool.fetchrow(
        "SELECT * FROM products WHERE id = $1", product_id
    )


async def get_products(pool: asyncpg.Pool, ):
    """ВСЕ ДОСТУПНЫЕ ТОВАРЫ"""

    return await pool.fetch(
        "SELECT * FROM products WHERE available = TRUE"
    )


#----------Корзина----------



async def get_cart(pool: asyncpg.Pool, telegram_id: int):
    """Корзина пользователя с данными товаров"""

    return await pool.fetch("""
                            SELECT p.name, p.price, c.quantity, (p.price * c.quantity) AS total
                            FROM cart_items c
                            JOIN products p ON p.id = c.product_id
                            WHERE c.telegram_id = $1
""", telegram_id)


async def add_to_cart(pool: asyncpg.Pool, telegram_id: int, product_id, quantity = 1):
    """Добавляет в корзину или увеличивает количеств товаров в ней"""

    await pool.execute("""
                       INSERT INTO cart_items (telegram_id, product_id, quantity)
                       VALUES ($1, $2, $3)
                       ON CONFLICT (telegram_id, product_id) DO UPDATE
                       SET quantity = cart_items.quantity + $3
""", telegram_id, product_id, quantity)
    

async def remove_from_cart(pool: asyncpg.Pool, telegram_id: int, product_id: int):
    """Удалить товар из корзины"""

    await pool.execute("""
                       DELETE FROM cart_items
                       WHERE telegram_id = $1 AND product_id = $2
""", telegram_id, product_id)
    

async def clear_cart(pool: asyncpg.Pool, telegram_id: int):
    """Очищает корзину"""

    await pool.execute("""
                       DELETE FROM cart_items
                       WHERE telegram_id = $1
""", telegram_id)


async def get_cart_total(pool: asyncpg.Pool, telegram_id: int) -> float:
    """Возвращает сумму корзины"""

    result = await pool.fetchval("""
                                 SELECT SUM(p.price * c.quantity)
                                 FROM cart_items c
                                 JOIN products p ON p.id = c.product_id
                                 WHERE c.telegram_id = $1
""", telegram_id)
    return float(result or 0)
