from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `ddata` ADD `component_id` INT NOT NULL  COMMENT '组件';
        ALTER TABLE `ddata` ADD CONSTRAINT `fk_ddata_componen_27bd013d` FOREIGN KEY (`component_id`) REFERENCES `component` (`id`) ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `ddata` DROP FOREIGN KEY `fk_ddata_componen_27bd013d`;
        ALTER TABLE `ddata` DROP COLUMN `component_id`;"""
