from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `component` ALTER COLUMN `life_forecast` SET DEFAULT -1;
        ALTER TABLE `component` MODIFY COLUMN `model_id` INT   COMMENT '模型';
        ALTER TABLE `component` MODIFY COLUMN `status` INT   COMMENT '组件状态';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `component` ALTER COLUMN `life_forecast` DROP DEFAULT;
        ALTER TABLE `component` MODIFY COLUMN `model_id` INT NOT NULL  COMMENT '模型';
        ALTER TABLE `component` MODIFY COLUMN `status` INT NOT NULL  COMMENT '组件状态';"""
