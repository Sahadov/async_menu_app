from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload

from db.db_setup import async_session_maker
from db.models.dish import Dish
from db.models.menu import Menu
from db.models.submenu import SubMenu
from pydantic_schemas.menu import MenuCreate


class SQLAlchemyRepository():  # AbstractRepository
    model = None

    async def get_menus(self):
        async with async_session_maker() as session:
            menus = await session.execute(select(self.model))
            return list(menus.scalars())

    async def create_menu(self, new_menu: MenuCreate):
        async with async_session_maker() as session:
            db_menu = self.model(**new_menu.model_dump())  # type: ignore
            session.add(db_menu)
            await session.commit()
            await session.refresh(db_menu)
            db_menu_dict = db_menu.__dict__
            db_menu_dict['id'] = str(db_menu_dict['id'])

            return db_menu_dict

    async def get_menu(self, menu_id: int):
        async with async_session_maker() as session:

            try:
                # получаем конкретное меню
                db_menu = await session.execute(select(self.model).where(self.model.id == menu_id))  # type: ignore
                db_menu_dict = db_menu.scalars().all()[0]

                # получаем список подменю и считаем его длину
                db_submenu = await session.execute(select(SubMenu).where(SubMenu.parent_id == menu_id))
                db_submenu_list = db_submenu.scalars().all()
                db_menu_dict.submenus_count = len(db_submenu_list)

                # получаем список блюд и считаем его длину
                db_dishes = await session.execute(select(Dish).where(Dish.main_menu_id == menu_id))
                db_dishes_list = db_dishes.scalars().all()
                db_menu_dict.dishes_count = len(db_dishes_list)

                db_menu_dict.id = str(db_menu_dict.id)

                return db_menu_dict
            except IndexError:
                raise HTTPException(status_code=404, detail='menu not found')

    async def delete_menu(self, menu_id: int):
        async with async_session_maker() as session:
            db_menu = await session.execute(delete(self.model).where(self.model.id == menu_id))  # type: ignore
            await session.commit()
            return db_menu

    async def update_menu(self, menu_id: int, title: str, description: str):
        async with async_session_maker() as session:
            db_menu = await session.get(self.model, menu_id)

            db_menu.title = title
            db_menu.description = description

            await session.commit()
            await session.refresh(db_menu)

            db_menu_dict = db_menu.__dict__
            db_submenu = await session.execute(select(SubMenu).where(SubMenu.parent_id == menu_id))
            db_submenu_list = db_submenu.scalars().all()
            db_menu_dict['submenus_count'] = len(db_submenu_list)

            db_dishes = await session.execute(select(Dish).where(Dish.main_menu_id == menu_id))
            db_dishes_list = db_dishes.scalars().all()
            db_menu_dict['dishes_count'] = len(db_dishes_list)

            return db_menu

    async def get_full_menus(self):
        async with async_session_maker() as session:
            result = await session.execute(
                select(Menu).options(
                    selectinload(Menu.submenus).selectinload(SubMenu.dishes)
                )
            )
            menus = result.scalars().all()
            return menus
