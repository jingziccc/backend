from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `mmodel` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL  COMMENT '模型名称',
    `style` VARCHAR(50) NOT NULL  COMMENT '模型风格',
    `uploaded_time` DATETIME(6) NOT NULL  COMMENT '上传时间' DEFAULT CURRENT_TIMESTAMP(6),
    `status` INT NOT NULL  COMMENT '训练状态',
    `description` LONGTEXT NOT NULL  COMMENT '描述'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `user` (
    `username` VARCHAR(50) NOT NULL  PRIMARY KEY COMMENT '用户名',
    `hashed_password` VARCHAR(50) NOT NULL  COMMENT '密码',
    `email` VARCHAR(50) NOT NULL  COMMENT '邮箱',
    `phone` VARCHAR(50) NOT NULL  COMMENT '电话',
    `role` INT NOT NULL  COMMENT '角色',
    `avatar` VARCHAR(1023) NOT NULL  COMMENT '头像'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `component` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL  COMMENT '组件名称',
    `status` INT NOT NULL  COMMENT '组件状态',
    `life_forecast` INT NOT NULL  COMMENT '寿命预测',
    `location` VARCHAR(50) NOT NULL  COMMENT '位置',
    `updated_time` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6),
    `model_id` INT NOT NULL COMMENT '模型',
    `user_id` VARCHAR(50) NOT NULL COMMENT '用户',
    CONSTRAINT `fk_componen_mmodel_f4533986` FOREIGN KEY (`model_id`) REFERENCES `mmodel` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_componen_user_4f29eeaa` FOREIGN KEY (`user_id`) REFERENCES `user` (`username`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
