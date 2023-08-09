# from abc import ABC, abstractmethod

from fastapi import HTTPException
from sqlalchemy import delete, select

from db.db_setup import async_session_maker
from db.models.dish import Dish

'''
class AbstractRepository(ABC):

    @abstractmethod
    async def get_submenus(self):
        raise NotImplementedError

    @abstractmethod
    async def create_submenu(self):
        raise NotImplementedError

    @abstractmethod
    async def get_submenu(self):
        raise NotImplementedError

    @abstractmethod
    async def delete_submenu(self):
        raise NotImplementedError

    @abstractmethod
    async def update_submenu(self):
        raise NotImplementedError
'''


class SQLAlchemyRepository():  # AbstractRepository
    model = None

    async def get_submenus(self, menu_id: int):
        async with async_session_maker() as session:
            db_menu = await session.execute(self.model.__table__.select()  # type: ignore
                                            .where(self.model.parent_id == menu_id))  # type: ignore
            return db_menu.all()

    async def create_submenu(self, new_menu, menu_id: int):
        async with async_session_maker() as session:
            db_menu = self.model(title=new_menu.title, description=new_menu.description,
                                 parent_id=menu_id)  # type: ignore
            session.add(db_menu)
            await session.commit()
            await session.refresh(db_menu)
            db_menu_dict = db_menu.__dict__
            db_menu_dict['id'] = str(db_menu_dict['id'])
            db_menu_dict['parent_id'] = str(db_menu_dict['parent_id'])
            return db_menu_dict

    async def get_submenu(self, menu_id: int, submenu_id: int):
        async with async_session_maker() as session:
            try:
                db_menu = await session.execute(select(self.model).where(self.model.id == submenu_id)  # type: ignore
                                                .where(self.model.parent_id == menu_id))  # type: ignore
                db_menu_dict = db_menu.scalars().all()[0]

                db_dishes = await session.execute(select(Dish).where(Dish.parent_id == submenu_id))
                db_dishes_list = db_dishes.scalars().all()
                db_menu_dict.dishes_count = len(db_dishes_list)

                db_menu_dict.id = str(db_menu_dict.id)

                return db_menu_dict
            except IndexError:
                raise HTTPException(status_code=404, detail='submenu not found')

    async def delete_submenu(self, menu_id: int, submenu_id: int):
        async with async_session_maker() as session:
            db_menu = await session.execute(delete(self.model).where(self.model.id == submenu_id)  # type: ignore
                                            .where(self.model.parent_id == menu_id))  # type: ignore
            await session.commit()

            return db_menu

    async def update_submenu(self, menu_id: int, submenu_id: int, title: str, description: str):
        async with async_session_maker() as session:
            db_menu = await session.get(self.model, submenu_id)

            db_menu.title = title
            db_menu.description = description

            await session.commit()
            await session.refresh(db_menu)

            db_menu_dict = db_menu.__dict__
            db_dishes = await session.execute(select(Dish).where(Dish.main_menu_id == menu_id))
            db_dishes_list = db_dishes.scalars().all()
            db_menu_dict['dishes_count'] = len(db_dishes_list)

            return db_menu
