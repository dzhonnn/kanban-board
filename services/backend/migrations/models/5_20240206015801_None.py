from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(20) NOT NULL UNIQUE,
    "email" VARCHAR(50) NOT NULL UNIQUE,
    "password" VARCHAR(128) NOT NULL
);
CREATE TABLE IF NOT EXISTS "sections" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(30) NOT NULL,
    "author_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "notes" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(30) NOT NULL,
    "description" VARCHAR(225),
    "comments" TEXT,
    "deadline" DATE NOT NULL,
    "section_id" INT NOT NULL REFERENCES "sections" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
