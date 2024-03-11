from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `mmodel` ADD `user_id` VARCHAR(50)   COMMENT '用户';
        ALTER TABLE `mmodel` ADD CONSTRAINT `fk_mmodel_user_69801b5b` FOREIGN KEY (`user_id`) REFERENCES `user` (`username`) ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `mmodel` DROP FOREIGN KEY `fk_mmodel_user_69801b5b`;
        ALTER TABLE `mmodel` DROP COLUMN `user_id`;"""
