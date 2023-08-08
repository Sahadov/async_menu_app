from typing import List

import fastapi
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.dishes import DishRepository

from db.db_setup import get_async_session
from pydantic_schemas.dish import DishCreate, Dish
from services.dish_service import DishService





router = fastapi.APIRouter()




@router.get('/dishes', response_model=List[Dish])
async def get_dishes(menu_id: int, submenu_id: int,
                     response: DishService = Depends()):
    return await response.read_dishes(submenu_id=submenu_id, menu_id=menu_id)


@router.post('/dishes', status_code=201)
async def create_new_dish(menu_id: int, submenu_id: int, new_menu: DishCreate,
                    response: DishService = Depends()):
    return await response.create_dish(new_menu=new_menu, submenu_id=submenu_id, menu_id=menu_id)


@router.get('/dishes/{dish_id}')
async def get_dish(menu_id: int, submenu_id: int, dish_id: int,
                   response: DishService = Depends()):
    return await response.read_dish(dish_id=dish_id, submenu_id=submenu_id, menu_id=menu_id)


@router.patch('/dishes/{dish_id}')
async def change_dish(menu_id: int, submenu_id: int, dish_id: int, menu: DishCreate,
                     response: DishService = Depends()):
    return await response.update_dish(dish_id=dish_id, menu=menu, submenu_id=submenu_id, menu_id=menu_id)


@router.delete('/dishes/{dish_id}')
async def delete_dish(menu_id: int, submenu_id: int, dish_id: int,
                      response: DishService = Depends()):
    return await response.delete_dish(dish_id=dish_id, submenu_id=submenu_id, menu_id=menu_id)