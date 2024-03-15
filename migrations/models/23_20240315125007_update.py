from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `component` ADD `description` LONGTEXT   COMMENT '描述';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `component` DROP COLUMN `description`;"""
