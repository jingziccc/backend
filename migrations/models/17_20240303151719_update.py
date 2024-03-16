from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `mmodel` CHANGE model_file modelfile LONGBLOB;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `mmodel` CHANGE modelfile model_file LONGBLOB;"""
