from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `mmodel` ADD `model_file` LONGBLOB NOT NULL  COMMENT '模型文件';
        ALTER TABLE `mmodel` DROP COLUMN `url`;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `mmodel` ADD `url` VARCHAR(1023)   COMMENT '模型地址';
        ALTER TABLE `mmodel` DROP COLUMN `model_file`;"""
