from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `component` ADD `pic` LONGBLOB   COMMENT '图片';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `component` DROP COLUMN `pic`;"""
