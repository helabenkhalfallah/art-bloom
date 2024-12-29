from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "artwork" ALTER COLUMN "place_of_origin" TYPE TEXT USING "place_of_origin"::TEXT;
        ALTER TABLE "artwork" ALTER COLUMN "style_title" TYPE TEXT USING "style_title"::TEXT;
        ALTER TABLE "artwork" ALTER COLUMN "artist_title" TYPE TEXT USING "artist_title"::TEXT;
        ALTER TABLE "artwork" ALTER COLUMN "classification_title" TYPE TEXT USING "classification_title"::TEXT;
        ALTER TABLE "artwork" ALTER COLUMN "title" TYPE TEXT USING "title"::TEXT;
        ALTER TABLE "artwork" ALTER COLUMN "medium_display" TYPE TEXT USING "medium_display"::TEXT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "artwork" ALTER COLUMN "place_of_origin" TYPE VARCHAR(255) USING "place_of_origin"::VARCHAR(255);
        ALTER TABLE "artwork" ALTER COLUMN "style_title" TYPE VARCHAR(255) USING "style_title"::VARCHAR(255);
        ALTER TABLE "artwork" ALTER COLUMN "artist_title" TYPE VARCHAR(255) USING "artist_title"::VARCHAR(255);
        ALTER TABLE "artwork" ALTER COLUMN "classification_title" TYPE VARCHAR(255) USING "classification_title"::VARCHAR(255);
        ALTER TABLE "artwork" ALTER COLUMN "title" TYPE VARCHAR(255) USING "title"::VARCHAR(255);
        ALTER TABLE "artwork" ALTER COLUMN "medium_display" TYPE VARCHAR(255) USING "medium_display"::VARCHAR(255);"""
