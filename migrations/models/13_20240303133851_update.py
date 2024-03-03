from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `mmodel` MODIFY COLUMN `status` VARCHAR(10) NOT NULL  COMMENT '模型状态';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `mmodel` MODIFY COLUMN `status` INT NOT NULL  COMMENT '训练状态';"""
