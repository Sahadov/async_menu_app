from typing import List

import fastapi
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.submenus import SubMenuRepository

from db.db_setup import get_async_session
from pydantic_schemas.submenu import SubMenuCreate, SubMenu
from services.submenu_service import SubMenuService




router = fastapi.APIRouter()



@router.get('/submenus', response_model=List[SubMenu])
async def read_submenus(menu_id: int, response: SubMenuService = Depends()):
    return await response.read_submenus(menu_id=menu_id)


@router.post('/submenus', status_code=201)
async def create_new_submenu(new_menu: SubMenuCreate, menu_id: int,
                       response: SubMenuService = Depends()):
    return await response.create_submenu(new_menu=new_menu, menu_id=menu_id)


@router.get('/submenus/{submenu_id}')
async def read_submenu(menu_id: int, submenu_id: int,
                      response: SubMenuService = Depends()):
    return await response.read_submenu(submenu_id=submenu_id, menu_id=menu_id)



@router.patch('/submenus/{submenu_id}')
async def change_submenu(menu_id: int, submenu_id: int, menu: SubMenuCreate,
                        response: SubMenuService = Depends()):
    return await response.update_submenu(submenu_id=submenu_id, menu=menu, menu_id=menu_id)


@router.delete('/submenus/{submenu_id}')
async def delete_submenu(menu_id: int, submenu_id: int,
                         response: SubMenuService = Depends()):
    return await response.del_submenu(submenu_id=submenu_id, menu_id=menu_id)
