from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "artwork" ADD "description" TEXT;
        ALTER TABLE "artwork" ADD "date_start" INT;
        ALTER TABLE "artwork" ADD "term_titles" JSONB;
        ALTER TABLE "artwork" ADD "artist_title" VARCHAR(255);
        ALTER TABLE "artwork" ADD "medium_display" VARCHAR(255);
        ALTER TABLE "artwork" ADD "thumbnail" VARCHAR(255);
        ALTER TABLE "artwork" ADD "category_titles" JSONB;
        ALTER TABLE "artwork" ADD "style_title" VARCHAR(255);
        ALTER TABLE "artwork" ADD "material_titles" JSONB;
        ALTER TABLE "artwork" ADD "artist_display" TEXT;
        ALTER TABLE "artwork" ADD "short_description" TEXT;
        ALTER TABLE "artwork" ADD "place_of_origin" VARCHAR(255);
        ALTER TABLE "artwork" ADD "date_display" VARCHAR(100);
        ALTER TABLE "artwork" ADD "classification_title" VARCHAR(255);
        ALTER TABLE "artwork" ADD "date_end" INT;
        ALTER TABLE "artwork" ALTER COLUMN "title" DROP NOT NULL;
        ALTER TABLE "artwork" ALTER COLUMN "title" TYPE VARCHAR(255) USING "title"::VARCHAR(255);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "artwork" DROP COLUMN "description";
        ALTER TABLE "artwork" DROP COLUMN "date_start";
        ALTER TABLE "artwork" DROP COLUMN "term_titles";
        ALTER TABLE "artwork" DROP COLUMN "artist_title";
        ALTER TABLE "artwork" DROP COLUMN "medium_display";
        ALTER TABLE "artwork" DROP COLUMN "thumbnail";
        ALTER TABLE "artwork" DROP COLUMN "category_titles";
        ALTER TABLE "artwork" DROP COLUMN "style_title";
        ALTER TABLE "artwork" DROP COLUMN "material_titles";
        ALTER TABLE "artwork" DROP COLUMN "artist_display";
        ALTER TABLE "artwork" DROP COLUMN "short_description";
        ALTER TABLE "artwork" DROP COLUMN "place_of_origin";
        ALTER TABLE "artwork" DROP COLUMN "date_display";
        ALTER TABLE "artwork" DROP COLUMN "classification_title";
        ALTER TABLE "artwork" DROP COLUMN "date_end";
        ALTER TABLE "artwork" ALTER COLUMN "title" SET NOT NULL;
        ALTER TABLE "artwork" ALTER COLUMN "title" TYPE VARCHAR(50) USING "title"::VARCHAR(50);"""
