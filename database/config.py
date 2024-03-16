CONFIG = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",  # 数据库类型
            "credentials": {
                "host": "111.229.169.56",
                "port": "3306",
                "user": "tzb",
                "password": "6zinnjSCChXFH647",
                "database": "tzb"
            },
        },
    },
    "apps": {
        "models": {
            "models": ["database.models", "aerich.models"],
            "default_connection": "default",
        }
    },
}
