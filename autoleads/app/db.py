import aiosqlite
import json
from typing import Dict
from logger import Logger
import asyncio

class Database:
    def __init__(self, db_name: str, logger: Logger):
        self.db_name = db_name
        self.logger = logger
        self.lock = asyncio.Lock()

    async def create_amazon_product_table(self):
        columns = {
            "id": "INTEGER PRIMARY KEY",
            "ASIN": "TEXT UNIQUE NOT NULL",
            "UPCS": "TEXT",
            "ASIN_data": "TEXT",
            "UPCS_data": "TEXT",
            "status": "INTEGER"
        }
        await self.create_table('AmazonProduct', columns)

    async def table_exists(self, table_name: str):
        async with aiosqlite.connect(self.db_name) as db:
            cur = await db.cursor()
            await cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
            result = await cur.fetchone()
            return result is not None

    async def get_table_columns(self, table_name: str):
        async with aiosqlite.connect(self.db_name) as db:
            cur = await db.cursor()
            try:
                await cur.execute(f'PRAGMA table_info({table_name})')
                existing_columns = await cur.fetchall()
                return [column[1] for column in existing_columns]
            except Exception as e:
                self.logger.log_and_write_error(f'{self.db_name}.{table_name}.get_table_columns', e)

    async def create_table(self, table_name: str, columns: Dict[str, str]):
        err = None
        async with aiosqlite.connect(self.db_name) as db:
            cur = await db.cursor()
            try:
                if not await self.table_exists(table_name):
                    cols = ', '.join([f'{colname} {coltype}' for colname, coltype in columns.items()])
                    await cur.execute(f'CREATE TABLE {table_name} ({cols})')

                existing_columns = await self.get_table_columns(table_name)

                for colname, coltype in columns.items():
                    if colname not in existing_columns:
                        await cur.execute(f'ALTER TABLE {table_name} ADD COLUMN {colname} {coltype}')
                        existing_columns.append(colname)
                    
                for column in existing_columns:
                    if column not in columns:
                        desired_columns = [col for col in existing_columns if col != column]
                        await cur.execute(f'CREATE TABLE temp_table AS SELECT {", ".join(desired_columns)} FROM {table_name}')
                        await cur.execute(f'DROP TABLE {table_name}')
                        await cur.execute(f'ALTER TABLE temp_table RENAME TO {table_name}')
                    
                await db.commit()
            except Exception as e:
                err = e
            self.logger.log_and_write_error(f'{self.db_name}.{table_name}.create_table', err)

    async def delete_table(self, table_name):
        err = None
        async with aiosqlite.connect(self.db_name) as db:
            cur = await db.cursor()
            try:
                await cur.execute(f'DROP TABLE IF EXISTS {table_name}')
            except Exception as e:
                err = e
        self.logger.log_and_write_error(f'{self.db_name}.{table_name}.delete_table', err)

    async def insert_amazon_product(self, data):
        err = None
        data["ASIN_data"] = json.dumps(data.get("ASIN_data", ""))
        data["UPCS_data"] = json.dumps(data.get("UPCS_data", ""))
        data["status"] = int(data.get("status", True))

        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data.values()])

        async with aiosqlite.connect(self.db_name) as db:
            cur = await db.cursor()
            try:
                await cur.execute(f'INSERT INTO AmazonProduct ({columns}) VALUES ({placeholders})', list(data.values()))
                await db.commit()
            except Exception as e:
                err = e
        self.logger.log_and_write_error(f'{self.db_name}.AmazonProduct.insert_data', err)

    async def get_amazon_product(self, asin):
        err = None
        async with aiosqlite.connect(self.db_name) as db:
            cur = await db.cursor()
            try:
                await cur.execute(f'SELECT * FROM AmazonProduct WHERE ASIN = ?', (asin,))
                row = await cur.fetchone()
                if row:
                    return {"id": row[0], "ASIN": row[1], "UPCS": row[2], "ASIN_data": json.loads(row[3]), "UPCS_data": json.loads(row[4]), "status": bool(row[5])}
                else:
                    return None
            except Exception as e:
                err = e
        self.logger.log_and_write_error(f'{self.db_name}.AmazonProduct.get_data', err)
        return None

    async def update_amazon_product(self, asin, new_data):
        err = None
        if 'ASIN_data' in new_data:
            new_data["ASIN_data"] = json.dumps(new_data["ASIN_data"])
        if 'UPCS_data' in new_data:
            new_data["UPCS_data"] = json.dumps(new_data["UPCS_data"])
        if 'status' in new_data:
            new_data["status"] = int(new_data["status"])
        async with aiosqlite.connect(self.db_name) as db:
            cur = await db.cursor()
            set_clause = ', '.join([f'{k} = ?' for k in new_data.keys()])
            try:
                await cur.execute(f'UPDATE AmazonProduct SET {set_clause} WHERE ASIN = ?', list(new_data.values()) + [asin])
                await db.commit()
            except Exception as e:
                err = e
        self.logger.log_and_write_error(f'{self.db_name}.AmazonProduct.update_data', err)

    async def delete_amazon_product(self, asin):
        err = None
        async with aiosqlite.connect(self.db_name) as db:
            cur = await db.cursor()
            try:
                await cur.execute(f'DELETE FROM AmazonProduct WHERE ASIN = ?', (asin,))
                await db.commit()
            except Exception as e:
                err = e
        self.logger.log_and_write_error(f'{self.db_name}.AmazonProduct.delete_data', err)
    
    async def get_all_amazon_products_only_if_has_ASIN_data(self):
        err = None
        async with aiosqlite.connect(self.db_name) as db:
            cur = await db.cursor()
            try:
                await cur.execute('SELECT * FROM AmazonProduct')
                rows = await cur.fetchall()
                products = [{"ASIN": row[1], "has_ASIN_data": bool(row[3]), "status": bool(row[5])} for row in rows]
                return products
            except Exception as e:
                err = e
        self.logger.log_and_write_error(f'{self.db_name}.AmazonProduct.get_all_amazon_products', err)
        return None
