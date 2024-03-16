from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `mmodel` ALTER COLUMN `style` SET DEFAULT 'default';
        ALTER TABLE `user` MODIFY COLUMN `avatar` VARCHAR(1023)   COMMENT '头像';
        ALTER TABLE `user` ALTER COLUMN `role` SET DEFAULT 0;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` MODIFY COLUMN `avatar` VARCHAR(1023) NOT NULL  COMMENT '头像';
        ALTER TABLE `user` ALTER COLUMN `role` DROP DEFAULT;
        ALTER TABLE `mmodel` ALTER COLUMN `style` DROP DEFAULT;"""
