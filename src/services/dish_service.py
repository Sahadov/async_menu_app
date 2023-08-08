import redis  # type: ignore
from fastapi import Depends

from repositories.redis_cache import RedisCache, get_redis_client
from repositories.dishes import DishRepository
from pydantic_schemas.dish import DishCreate, Dish

class DishService:
    def __init__(self, dish_repository: DishRepository = Depends(),
                 redis_client: redis.Redis = Depends(get_redis_client)):
        self.dish_repository = dish_repository
        self.cache_client = RedisCache(redis_client)

    async def read_dishes(self, submenu_id: int, menu_id: int):
        cached = self.cache_client.get(f'all:{menu_id}:{submenu_id}')
        if cached is not None:
            return cached
        else:
            data = await self.dish_repository.get_dishes(submenu_id=submenu_id, menu_id=menu_id)
            self.cache_client.set(f'all:{menu_id}:{submenu_id}', data)
            return data

    async def create_dish(self, new_menu, submenu_id: int, menu_id: int):
        data = await self.dish_repository.create_dish(new_menu=new_menu, submenu_id=submenu_id, menu_id=menu_id)
        self.cache_client.set(f'{menu_id}:{submenu_id}:{data["id"]}', data)
        self.cache_client.clear_after_change(menu_id)
        return data

    async def read_dish(self, dish_id: int, submenu_id: int, menu_id: int):
        cached = self.cache_client.get(f'{menu_id}:{submenu_id}:{dish_id}')
        if cached is not None:
            return cached
        else:
            data = await self.dish_repository.get_dish(dish_id=dish_id, submenu_id=submenu_id, menu_id=menu_id)
            self.cache_client.set(f'{menu_id}:{submenu_id}:{dish_id}', data)
            return data

    async def update_dish(self, dish_id: int, menu: DishCreate, submenu_id: int, menu_id: int):
        data = await self.dish_repository.update_dish(dish_id=dish_id, submenu_id=submenu_id, menu_id=menu_id, title=menu.title, description=menu.description, price=menu.price)
        self.cache_client.set(f'{menu_id}:{submenu_id}:{dish_id}', data)
        self.cache_client.clear_after_change(menu_id)
        return data

    async def delete_dish(self, dish_id: int, submenu_id: int, menu_id: int):
        data = await self.dish_repository.delete_dish(dish_id=dish_id, submenu_id=submenu_id, menu_id=menu_id)
        self.cache_client.delete(f'{menu_id}:{submenu_id}:{dish_id}')
        self.cache_client.clear_after_change(menu_id)
        return data