from os import environ

TORTOISE_ORM = {
    "connections": {"default": environ.get("DATABASE_URL")},
    "apps": {
        "models": {
            "models": [
                "src.database.models", "aerich.models"
            ],
            "default_connetion": "default"
        }
    }
}
