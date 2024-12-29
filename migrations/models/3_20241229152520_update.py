from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "artwork" ALTER COLUMN "date_display" TYPE TEXT USING "date_display"::TEXT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "artwork" ALTER COLUMN "date_display" TYPE VARCHAR(100) USING "date_display"::VARCHAR(100);"""
