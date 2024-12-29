from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "artwork" ALTER COLUMN "thumbnail" TYPE TEXT USING "thumbnail"::TEXT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "artwork" ALTER COLUMN "thumbnail" TYPE VARCHAR(255) USING "thumbnail"::VARCHAR(255);"""
