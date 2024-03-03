from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `mmodel` ADD UNIQUE INDEX `uid_mmodel_name_9b3697` (`name`);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `mmodel` DROP INDEX `idx_mmodel_name_9b3697`;"""
