from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` MODIFY COLUMN `hashed_password` VARCHAR(128) NOT NULL  COMMENT '密码';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` MODIFY COLUMN `hashed_password` VARCHAR(50) NOT NULL  COMMENT '密码';"""
