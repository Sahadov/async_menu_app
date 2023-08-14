import redis  # type: ignore
from fastapi import BackgroundTasks, Depends

from pydantic_schemas.dish import DishCreate
from repositories.dishes import DishRepository
from repositories.redis_cache import AsyncRedisCache, get_async_redis_client


class DishService:
    def __init__(self, dish_repository: DishRepository = Depends(),
                 redis_client: redis.Redis = Depends(get_async_redis_client),
                 background_tasks: BackgroundTasks = None):
        self.dish_repository = dish_repository
        self.cache_client = AsyncRedisCache(redis_client)
        self.background_tasks = background_tasks

    async def read_dishes(self, submenu_id: int, menu_id: int):
        cached = await self.cache_client.get(f'all:{menu_id}:{submenu_id}')
        if cached is not None:
            return cached
        else:
            data = await self.dish_repository.get_dishes(submenu_id=submenu_id, menu_id=menu_id)
            await self.cache_client.set(f'all:{menu_id}:{submenu_id}', data, self.background_tasks)
            return data

    async def create_dish(self, new_menu, submenu_id: int, menu_id: int):
        data = await self.dish_repository.create_dish(new_menu=new_menu, submenu_id=submenu_id, menu_id=menu_id)
        await self.cache_client.set(f'{menu_id}:{submenu_id}:{data["id"]}', data, self.background_tasks)
        await self.cache_client.clear_after_change(menu_id, self.background_tasks)
        return data

    async def read_dish(self, dish_id: int, submenu_id: int, menu_id: int):
        cached = await self.cache_client.get(f'{menu_id}:{submenu_id}:{dish_id}')
        if cached is not None:
            return cached
        else:
            data = await self.dish_repository.get_dish(dish_id=dish_id, submenu_id=submenu_id, menu_id=menu_id)
            await self.cache_client.set(f'{menu_id}:{submenu_id}:{dish_id}', data, self.background_tasks)
            return data

    async def update_dish(self, dish_id: int, menu: DishCreate, submenu_id: int, menu_id: int):
        data = await self.dish_repository.update_dish(dish_id=dish_id, submenu_id=submenu_id, menu_id=menu_id, title=menu.title, description=menu.description, price=menu.price)
        await self.cache_client.set(f'{menu_id}:{submenu_id}:{dish_id}', data, self.background_tasks)
        await self.cache_client.clear_after_change(menu_id, self.background_tasks)
        return data

    async def delete_dish(self, dish_id: int, submenu_id: int, menu_id: int):
        data = await self.dish_repository.delete_dish(dish_id=dish_id, submenu_id=submenu_id, menu_id=menu_id)
        await self.cache_client.delete(f'{menu_id}:{submenu_id}:{dish_id}', self.background_tasks)
        await self.cache_client.clear_after_change(menu_id, self.background_tasks)
        return data
