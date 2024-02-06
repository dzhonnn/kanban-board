from os import environ

class TortoiseConfig():
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

    @staticmethod
    def get():
        return TortoiseConfig.TORTOISE_ORM


conf: dict = TortoiseConfig.get()