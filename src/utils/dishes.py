# from abc import ABC, abstractmethod

from fastapi import HTTPException
from sqlalchemy import delete, select

from db.db_setup import async_session_maker

'''
class AbstractRepository(ABC):

    @abstractmethod
    async def get_dishes(self):
        raise NotImplementedError

    @abstractmethod
    async def create_dish(self):
        raise NotImplementedError

    @abstractmethod
    async def get_dish(self):
        raise NotImplementedError

    @abstractmethod
    async def delete_dish(self):
        raise NotImplementedError

    @abstractmethod
    async def update_dish(self):
        raise NotImplementedError
'''


class SQLAlchemyRepository():  # AbstractRepository
    model = None

    async def get_dishes(self, menu_id: int, submenu_id: int):
        async with async_session_maker() as session:
            db_menu = await session.execute(self.model.__table__.select()  # type: ignore
                                            .where(self.model.parent_id == submenu_id))  # type: ignore
            return db_menu.all()

    async def create_dish(self, new_menu, menu_id: int, submenu_id: int):
        async with async_session_maker() as session:
            db_menu = self.model(title=new_menu.title, description=new_menu.description,  # type: ignore
                                 parent_id=submenu_id, price=new_menu.price, main_menu_id=menu_id)  # type: ignore
            session.add(db_menu)
            await session.commit()
            await session.refresh(db_menu)
            db_menu_dict = db_menu.__dict__
            db_menu_dict['parent_id'] = str(db_menu_dict['parent_id'])
            db_menu_dict['price'] = str(db_menu_dict['price'])
            db_menu_dict['id'] = str(db_menu_dict['id'])
            return db_menu_dict

    async def get_dish(self, menu_id: int, submenu_id: int, dish_id: int):
        async with async_session_maker() as session:
            try:
                db_menu = await session.execute(select(self.model).where(self.model.id == dish_id)  # type: ignore
                                                .where(self.model.parent_id == submenu_id))  # type: ignore
                db_menu_dict = db_menu.scalars().all()[0]

                db_menu_dict.id = str(db_menu_dict.id)
                db_menu_dict.price = str(db_menu_dict.price)

                return db_menu_dict
            except IndexError:
                raise HTTPException(status_code=404, detail='dish not found')

    async def delete_dish(self, menu_id: int, submenu_id: int, dish_id: int):
        async with async_session_maker() as session:
            db_menu = await session.execute(delete(self.model).where(self.model.id == dish_id)  # type: ignore
                                            .where(self.model.parent_id == submenu_id))  # type: ignore
            await session.commit()

            return db_menu

    async def update_dish(self, menu_id: int, submenu_id: int, dish_id: int, title: str, description: str, price: float):
        async with async_session_maker() as session:
            db_menu = await session.get(self.model, dish_id)

            db_menu.title = title
            db_menu.description = description
            db_menu.price = price

            await session.commit()
            await session.refresh(db_menu)

            db_menu.price = str(db_menu.price)

            return db_menu
