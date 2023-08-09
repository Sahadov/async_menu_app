import redis  # type: ignore
from fastapi import FastAPI

from api import dishes, menus, submenus
from db.db_setup import Base, engine

# menu.Base.metadata.create_all(bind=engine)
# submenu.Base.metadata.create_all(bind=engine)
# dish.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title='ASYNC Menu App'
)

app.include_router(menus.router, prefix='/api/v1', tags=['Menus'])
app.include_router(submenus.router, prefix='/api/v1/menus/{menu_id}', tags=['Submenus'])
app.include_router(dishes.router, prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}', tags=['Dishes'])

redis_client = redis.Redis(host='redis', port=5370, db=0)


@app.on_event('startup')
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
