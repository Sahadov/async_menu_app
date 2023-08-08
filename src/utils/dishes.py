from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, delete
from db.db_setup import async_session_maker

from pydantic_schemas.dish import DishCreate
from db.models.dish import Dish
from fastapi import HTTPException




class AbstractRepository(ABC):

    @abstractmethod
    async def get_dishes():
        raise NotImplementedError
    
    @abstractmethod
    async def create_dish():
        raise NotImplementedError
    
    @abstractmethod
    async def get_dish():
        raise NotImplementedError
    
    @abstractmethod
    async def delete_dish():
        raise NotImplementedError
    
    @abstractmethod
    async def update_dish():
        raise NotImplementedError
    


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def get_dishes(self, menu_id: int, submenu_id: int):
        async with async_session_maker() as session:
            db_menu = await session.execute(self.model.__table__.select().where(self.model.parent_id == submenu_id))
            return db_menu.all()
        
    async def create_dish(self, new_menu, menu_id: int, submenu_id:int):
        async with async_session_maker() as session:
            db_menu = self.model(title=new_menu.title, description=new_menu.description, parent_id=submenu_id, price=new_menu.price, main_menu_id=menu_id)
            session.add(db_menu)
            await session.commit()
            await session.refresh(db_menu)
            db_menu_dict = db_menu.__dict__
            db_menu_dict["parent_id"] = str(db_menu_dict["parent_id"])
            db_menu_dict["price"] = str(db_menu_dict["price"])
            db_menu_dict["id"] = str(db_menu_dict["id"])
            return db_menu_dict


    async def get_dish(self, menu_id: int, submenu_id: int, dish_id: int):
        async with async_session_maker() as session:
            try:
                db_menu = await session.execute(select(self.model).where(self.model.id == dish_id).where(self.model.parent_id == submenu_id))
                db_menu_dict = db_menu.scalars().all()[0]

                db_menu_dict.id = str(db_menu_dict.id)
                db_menu_dict.price = str(db_menu_dict.price)
                
                
                return db_menu_dict
            except:
                raise HTTPException(status_code=404, detail="dish not found")

        
    async def delete_dish(self, menu_id: int, submenu_id: int, dish_id: int):
        async with async_session_maker() as session:
            db_menu = await session.execute(delete(self.model).where(self.model.id == dish_id).where(self.model.parent_id == submenu_id))
            await session.commit()
    
            return db_menu
        
    async def update_dish(self, menu_id: int, submenu_id: int, dish_id:int, title: str, description: str, price:float):
        async with async_session_maker() as session:
            db_menu = await session.get(self.model, dish_id)

            db_menu.title = title
            db_menu.description = description
            db_menu.price = price

            await session.commit()
            await session.refresh(db_menu)

            db_menu.price = str(db_menu.price)


            return db_menu

    