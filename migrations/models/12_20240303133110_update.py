from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `mmodel` ADD `md5` VARCHAR(32) NOT NULL UNIQUE COMMENT 'md5值';
        ALTER TABLE `mmodel` ADD UNIQUE INDEX `uid_mmodel_md5_4987bc` (`md5`);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `mmodel` DROP INDEX `idx_mmodel_md5_4987bc`;
        ALTER TABLE `mmodel` DROP COLUMN `md5`;"""
