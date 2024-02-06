from tortoise import Tortoise


async def init_orm(config, generate_schemas):
    print("Inited")
    await Tortoise.init(config=config)
    if generate_schemas:
        await Tortoise.generate_schemas()


async def close_orm():
    await Tortoise.close_connections()
