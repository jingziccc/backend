from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `ddata` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `file` LONGBLOB NOT NULL  COMMENT '数据文件',
    `name` VARCHAR(50)   COMMENT '数据名称',
    `time` DATETIME(6) NOT NULL  COMMENT '上传时间' DEFAULT CURRENT_TIMESTAMP(6),
    `result` LONGTEXT   COMMENT '结果'
) CHARACTER SET utf8mb4;
        DROP TABLE IF EXISTS `data`;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `ddata`;"""
