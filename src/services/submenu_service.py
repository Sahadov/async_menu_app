import redis  # type: ignore
from fastapi import Depends

from pydantic_schemas.submenu import SubMenuCreate
from repositories.redis_cache import RedisCache, get_redis_client
from repositories.submenus import SubMenuRepository


class SubMenuService:
    def __init__(self, submenu_repository: SubMenuRepository = Depends(),
                 redis_client: redis.Redis = Depends(get_redis_client)):
        self.submenu_repository = submenu_repository
        self.cache_client = RedisCache(redis_client)

    async def read_submenus(self, menu_id: int):
        cached = self.cache_client.get(f'all:{menu_id}')
        if cached is not None:
            return cached
        else:
            data = await self.submenu_repository.get_submenus(menu_id)
            # data.id = str(data.id)
            self.cache_client.set(f'all:{menu_id}', data)
            return data

    async def create_submenu(self, new_menu: SubMenuCreate, menu_id: int):
        data = await self.submenu_repository.create_submenu(new_menu, menu_id)
        data['id'] = str(data['id'])
        data['parent_id'] = str(data['parent_id'])
        self.cache_client.set(f'{menu_id}:{data["id"]})', data)
        self.cache_client.clear_after_change(menu_id)
        return data

    async def read_submenu(self, menu_id: int, submenu_id: int):
        cached = self.cache_client.get(f'{menu_id}:{submenu_id}')
        if cached is not None:
            return cached
        else:
            data = await self.submenu_repository.get_submenu(menu_id=menu_id, submenu_id=submenu_id)
            self.cache_client.set(f'{menu_id}:{submenu_id}', data)
            return data

    async def update_submenu(self, submenu_id: int, menu: SubMenuCreate, menu_id: int):
        data = await self.submenu_repository.update_submenu(submenu_id=submenu_id, menu_id=menu_id, title=menu.title, description=menu.description)
        self.cache_client.set(f'{menu_id}:{submenu_id}', data)
        self.cache_client.clear_after_change(menu_id)
        return data

    async def del_submenu(self, submenu_id: int, menu_id: int):
        data = await self.submenu_repository.delete_submenu(submenu_id=submenu_id, menu_id=menu_id)
        self.cache_client.delete(f'{menu_id}:{submenu_id}')
        self.cache_client.clear_after_change(menu_id)
        return data
