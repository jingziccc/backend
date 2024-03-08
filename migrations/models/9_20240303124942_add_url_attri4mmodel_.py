from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `mmodel` ADD `url` VARCHAR(1023)   COMMENT '模型地址';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `mmodel` DROP COLUMN `url`;"""
