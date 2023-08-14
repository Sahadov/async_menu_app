import fastapi
from fastapi import Depends

from pydantic_schemas.menu import Menu, MenuCreate
from services.menu_service import MenuService

router = fastapi.APIRouter()


@router.get('/menus', response_model=list[Menu])
async def read_menus(response: MenuService = Depends()):
    return await response.read_menus()


@router.post('/menus', status_code=201)
async def create_new_menu(menu: MenuCreate, response: MenuService = Depends()):
    return await response.create_menu(menu)


@router.get('/menus/full')
async def get_full_menus(response: MenuService = Depends()):
    return await response.read_full_menus()


@router.get('/menus/{menu_id}')
async def read_menu(menu_id: int, response: MenuService = Depends()):
    return await response.read_menu(menu_id)


@router.patch('/menus/{menu_id}')
async def change_menu(menu_id: int, menu: MenuCreate, response: MenuService = Depends()):
    return await response.update_menu(menu_id, menu)


@router.delete('/menus/{menu_id}')
async def delete_menu(menu_id: int, response: MenuService = Depends()):
    return await response.remove_menu(menu_id)
