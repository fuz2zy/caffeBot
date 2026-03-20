import logging


class Database:

    def __init__(self, pool):

        self.pool = pool
        self.logger = logging.getLogger(name=__name__)

    async def close_pool(self):
        await self.pool.close()


    async def init_db(self):

        await self.pool.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id BIGINT PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                phone TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        await self.pool.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                description TEXT,
                available BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                category TEXT NOT NULL,
                telegram_id_image TEXT NOT NULL,
                UNIQUE(name)
            )
        """)

        await self.pool.execute("""
            CREATE TABLE IF NOT EXISTS cart_items (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT NOT NULL,
                product_id INTEGER NOT NULL REFERENCES products(id),
                quantity INTEGER NOT NULL DEFAULT 1,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(telegram_id, product_id)
            )
        """)


    async def add_user(self, id: int, username: str, first_name: str, last_name: str):

        await self.pool.execute("""
                        INSERT INTO users (id)
                        VALUES ($1)
                        ON CONFLICT (id) DO UPDATE
                        SET username = $2, first_name = $3, last_name = $4
    """, id, username, first_name, last_name)


    async def get_user(self, telegram_id: int):

        return await self.pool.fetchrow(
            "SELECT * FROM users WHERE id = $1", telegram_id
        )


    async def get_users(self):

        return await self.pool.fetch(
            "SELECT * FROM users "
        )


    async def get_user_phone(self, user_id: int) -> str:

        result = await self.pool.fetchval(
            "SELECT phone FROM users WHERE id = $1", user_id
        )

        return str(result)


    async def add_user_phone(self, user_id: int, phone: str) -> None:
        await self.pool.execute(
            "UPDATE users SET phone = $2 WHERE id = $1", user_id, phone
        )
        self.logger.info(f"USER (id = {user_id}) verified his number (phone = {phone})")



    async def add_product(self, name: str, price: float, category: str, telegram_id_image: str, description: str = 'Описание товара отсутсвует'):

        await self.pool.execute("""
                        INSERT INTO products (name, price, description, category, telegram_id_image)
                        VALUES ($1, $2, $3, $4, $5)
                        ON CONFLICT (name) DO UPDATE
                        SET price=$2, description=$3
    """, name, price, description, category, telegram_id_image)


    async def delete_product(self, product_id: int):

        await self.pool.execute(
            "DELETE FROM products WHERE id = $1", product_id
        )


    async def hide_product(self, product_id: int):

        await self.fpool.execute(
            "UPDATE products SET available = FALSE WHERE id = $1", product_id
        )


    async def show_product(self, product_id: int):

        await self.pool.execute(
            "UPDATE products SET available = TRUE WHERE id = $1", product_id
        )


    async def get_product(self, product_id: int):

        return await self.pool.fetchrow(
            "SELECT * FROM products WHERE id = $1", product_id
        )


    async def get_products(self):

        return await self.pool.fetch(
            "SELECT * FROM products WHERE available = TRUE"
        )


    async def get_products_by_category(self, category):

        return await self.pool.fetch(
            "SELECT * FROM products WHERE available = TRUE AND category = $1", category
        )


    async def get_categories(self):
        rows = await self.pool.fetch(
            "SELECT DISTINCT category FROM products WHERE available = TRUE"
        )
        return [rows[row]["category"] for row in range(len(rows))]

    async def get_cart(self, telegram_id: int):

        return await self.pool.fetch("""
                                SELECT p.id, p.name, p.price, c.quantity, (p.price * c.quantity) AS total
                                FROM cart_items c
                                JOIN products p ON p.id = c.product_id
                                WHERE c.telegram_id = $1
    """, telegram_id)


    async def add_to_cart(self, telegram_id: int, product_id, quantity = 1):

        await self.pool.execute("""
                        INSERT INTO cart_items (telegram_id, product_id, quantity)
                        VALUES ($1, $2, $3)
                        ON CONFLICT (telegram_id, product_id) DO UPDATE
                        SET quantity = cart_items.quantity + $3
    """, telegram_id, product_id, quantity)
        

    async def remove_from_cart(self, telegram_id: int, product_id: int):

        await self.pool.execute("""
                        DELETE FROM cart_items
                        WHERE telegram_id = $1 AND product_id = $2
    """, telegram_id, product_id)
        

    async def clear_cart(self, telegram_id: int):

        await self.pool.execute("""
                        DELETE FROM cart_items
                        WHERE telegram_id = $1
    """, telegram_id)


    async def get_product_in_user_cart(self, telegram_id: int, product_id: int):
        
        await self.pool.execute("""
                        INSERT INTO cart_items (telegram_id, product_id, quantity)
                        VALUES ($1, $2, 0)
                        ON CONFLICT DO NOTHING
    """, telegram_id, product_id)

        result = await self.pool.fetchrow("""
                        SELECT * 
                        FROM cart_items c
                        JOIN products p ON p.id = c.product_id
                        WHERE telegram_id = $1 AND product_id = $2
                        
    """, telegram_id, product_id)
        
        return result


    async def get_cart_total(self, telegram_id: int) -> float:

        result = await self.pool.fetchval("""
                                    SELECT SUM(p.price * c.quantity)
                                    FROM cart_items c
                                    JOIN products p ON p.id = c.product_id
                                    WHERE c.telegram_id = $1
    """, telegram_id)
        return float(result or 0)
