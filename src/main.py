import redis  # type: ignore
from fastapi import FastAPI

from api import dishes, menus, submenus
from db.db_setup import Base, engine

app = FastAPI(
    title='YLAB Menu App'
)


app.include_router(menus.router, prefix='/api/v1', tags=['Menus'])
app.include_router(submenus.router, prefix='/api/v1/menus/{menu_id}', tags=['Submenus'])
app.include_router(dishes.router, prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}', tags=['Dishes'])

# redis_client = redis.Redis(host='redis', port=5370, db=0) для докера
redis_client = redis.Redis(host='localhost', port=6379, db=0)


@app.on_event('startup')
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
