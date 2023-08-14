import pickle
from typing import Any

import redis.asyncio as redis  # type: ignore
from fastapi import BackgroundTasks, Depends


def get_async_redis_pool():
    return redis.from_url('redis://redis:5370/0', decode_responses=False)
    # return redis.Redis(host='localhost', port=6379, db=0, decode_responses=False)


async def get_async_redis_client(redis_pool: redis.Redis = Depends(get_async_redis_pool)):
    return redis_pool


class AsyncRedisCache:
    def __init__(self, redis_pool: redis.Redis = Depends(get_async_redis_pool)):
        self.redis_pool = redis_pool
        self.ttl = 1800

    async def get(self, key: str) -> Any | None:
        data = await self.redis_pool.get(key)
        if data is not None:
            return pickle.loads(data)
        return None

    async def set(self, key: str, value: Any, background_tasks: BackgroundTasks):
        data = pickle.dumps(value)
        background_tasks.add_task(self._set_cache, key, data)

    async def _set_cache(self, key: str, data: Any) -> None:
        await self.redis_pool.setex(key, self.ttl, data)

    async def delete(self, key: str, background_tasks: BackgroundTasks):
        background_tasks.add_task(self._delete_cache, key)

    async def _delete_cache(self, key: str):
        await self.redis_pool.delete(key)

    async def clear_cache(self, pattern: str, background_tasks: BackgroundTasks):
        keys = [key async for key in self.redis_pool.scan_iter(pattern)]
        if keys:
            background_tasks.add_task(self._clear_keys, keys)

    async def _clear_keys(self, keys: list[str]):
        await self.redis_pool.delete(*keys)

    async def clear_after_change(self, menu_id: int | str, background_tasks: BackgroundTasks):
        await self.clear_cache(f'{menu_id}*', background_tasks)
        await self.clear_cache('all*', background_tasks)
