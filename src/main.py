from fastapi import FastAPI
import redis  # type: ignore

from api import menus, submenus, dishes
from db.db_setup import engine
from db.models import menu, submenu, dish




#menu.Base.metadata.create_all(bind=engine)
#submenu.Base.metadata.create_all(bind=engine)
#dish.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="ASYNC Menu App"
)

app.include_router(menus.router, prefix='/api/v1', tags=['Menus'])
app.include_router(submenus.router, prefix='/api/v1/menus/{menu_id}', tags=['Submenus'])
app.include_router(dishes.router, prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}', tags=['Dishes'])

redis_client = redis.Redis(host='localhost', port=6379, db=0)


