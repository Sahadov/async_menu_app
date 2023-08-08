from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, delete
from db.db_setup import async_session_maker

from pydantic_schemas.submenu import SubMenuCreate
from db.models.submenu import SubMenu
from db.models.submenu import SubMenu
from db.models.dish import Dish
from fastapi import HTTPException



class AbstractRepository(ABC):

    @abstractmethod
    async def get_submenus():
        raise NotImplementedError
    
    @abstractmethod
    async def create_submenu():
        raise NotImplementedError
    
    @abstractmethod
    async def get_submenu():
        raise NotImplementedError
    
    @abstractmethod
    async def delete_submenu():
        raise NotImplementedError
    
    @abstractmethod
    async def update_submenu():
        raise NotImplementedError
    


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def get_submenus(self, menu_id: int):
        async with async_session_maker() as session:
            db_menu = await session.execute(self.model.__table__.select().where(self.model.parent_id == menu_id))
            return db_menu.all()
        
    async def create_submenu(self, new_menu, menu_id: int):
        async with async_session_maker() as session:
            db_menu = self.model(title=new_menu.title, description=new_menu.description, parent_id=menu_id)
            session.add(db_menu)
            await session.commit()
            await session.refresh(db_menu)
            db_menu_dict = db_menu.__dict__
            db_menu_dict["id"] = str(db_menu_dict["id"])
            db_menu_dict["parent_id"] = str(db_menu_dict["parent_id"])
            return db_menu_dict


    async def get_submenu(self, menu_id: int, submenu_id: int):
        async with async_session_maker() as session:
            try:
                db_menu = await session.execute(select(self.model).where(self.model.id == submenu_id).where(self.model.parent_id == menu_id))
                db_menu_dict = db_menu.scalars().all()[0]
                
                db_dishes = await session.execute(select(Dish).where(Dish.parent_id == submenu_id))
                db_dishes_list = db_dishes.scalars().all()
                db_menu_dict.dishes_count = len(db_dishes_list)

                db_menu_dict.id = str(db_menu_dict.id)

                return db_menu_dict
            except:
                raise HTTPException(status_code=404, detail="submenu not found")
           

        
    async def delete_submenu(self, menu_id: int, submenu_id: int):
        async with async_session_maker() as session:
            db_menu = await session.execute(delete(self.model).where(self.model.id == submenu_id).where(self.model.parent_id == menu_id))
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
            db_menu_dict["dishes_count"] = len(db_dishes_list)

            return db_menu

    



   